import datetime, time
import platform
import simpy
import shapely.geometry
from simplekml import Kml, Style
import numpy as np

import openclsim.core as core
import openclsim.model as model
import openclsim.plot as plot

import halem
import halem.Mesh_maker as Mesh_maker
import halem.Functions as Functions
import halem.Calc_path as Calc_path

import pickle
import networkx as nx

import matplotlib.pyplot as plt
plt.style.use('ggplot')
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.interpolate import griddata

import netCDF4
from netCDF4 import Dataset, num2date
from scipy.spatial import Delaunay
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def interpolate(r, maxi, mini):
    return (maxi - mini)*r + mini

def connect_sites_with_path(data_from_site, data_to_site, data_node, path):
    Nodes = []
    Edges = []
    Site = type('Site', (core.Identifiable, # Give it a name
             core.Log,          # Allow logging of all discrete events
             core.Locatable,    # Add coordinates to extract distance information and visualize
             core.HasContainer, # Add information on the material available at the site
             core.HasResource), # Add information on serving equipment
    {})                         # The dictionary is empty because the site type is generic

    Node = type('Node', (core.Identifiable, # Give it a name
             core.Log,          # Allow logging of all discrete events
             core.Locatable),   # Add coordinates to extract distance information and visualize
    {})                         # The dictionary is empty because the site type is generic

    for i, j in enumerate(path):
        if i == 0:
            data_from_site["geometry"]=shapely.geometry.Point(path[i][0], path[i][1])
            Nodes.append(Site(**data_from_site))

        elif i == len(path) - 1:
            data_to_site["geometry"]=shapely.geometry.Point(path[i][0], path[i][1])
            Nodes.append(Site(**data_to_site))
            Edges.append([Nodes[i-1], Nodes[i]])
            
        else:
            data_node["geometry"]=shapely.geometry.Point(path[i][0], path[i][1])
            data_node["name"]='node-' + str(i)
            Nodes.append(Node(**data_node))
            Edges.append([Nodes[i-1], Nodes[i]])
            
    return Nodes, Edges

def compute_v_provider(v_empty, v_full):
    return lambda x: x * (v_full - v_empty) + v_empty

def compute_loading(rate):
    return lambda current_level, desired_level: (desired_level - current_level) / rate

def compute_unloading(rate):
    return lambda current_level, desired_level: (current_level - desired_level) / rate

def compute_cost(week_rate, fuel_rate):
    second_rate = week_rate/7/24/60/60
    return lambda travel_time, speed: (travel_time*second_rate + fuel_rate*travel_time * speed**3)

def compute_co2(fuel_rate):
    return lambda travel_time, speed: (fuel_rate*travel_time * speed**3)

def plot_route(hopper, Roadmap):
    x_r = np.arange(3.2,3.8, 0.001)
    y_r = np.arange(51,52, 0.01)
    y_r, x_r = np.meshgrid(y_r,x_r)

    WD_r = griddata((Roadmap.nodes[:,1], Roadmap.nodes[:,0]), Roadmap.WD[:,1], (x_r, y_r), method= 'linear')

    Hopper_route = hopper.log['Geometry']
    x_loc = []
    y_loc = []
    for G in Hopper_route:
        x_loc.append(G.x)
        y_loc.append(G.y)
    x_loc = np.array(x_loc)
    y_loc = np.array(y_loc)

    TT = hopper.log['Timestamp']
    Time = []

    for T in TT:
        TTT = T.timestamp()
        Time.append(TTT)

    Time= np.array(Time)
    Time = (Time - Time[0])/3600/24

    points = np.array([x_loc, y_loc]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig = plt.figure(figsize = (40,40))
    ax = plt.subplot(projection=ccrs.Mercator())

    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '10m', edgecolor='face', facecolor='cornflowerblue', zorder = 0))
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor='face', facecolor='cornflowerblue'))
    cval = np.arange(0,40,1)
    plt.contourf(x_r,y_r,WD_r, cval, alpha = 0.6,transform=ccrs.PlateCarree())
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='face', facecolor='palegoldenrod'))
    ax.coastlines(resolution='10m', color='darkgoldenrod', linewidth=3)

    plt.triplot(Roadmap.nodes[:,1], Roadmap.nodes[:,0], Roadmap.tria.simplices, linewidth = 0.8, color = 'k', label = 'Delauney edges', transform=ccrs.PlateCarree())

    norm = plt.Normalize(Time.min(), Time.max())
    lc = LineCollection(segments, linewidth = 5, cmap='rainbow', norm=norm, transform=ccrs.PlateCarree())

    lc.set_array(Time)
    line = ax.add_collection(lc)

    ax.set_extent([x_loc.min()*0.999, x_loc.max()*1.02, y_loc.min()*0.999, y_loc.max()*1.0001])
    plt.show()

class flow_2D_FM_100m():
    def __init__(self, name):
        nc = Dataset(name)

        t = nc.variables['time'][:]
        t0 = "22/12/2012 00:00:00"
        d = datetime.datetime.strptime(t0, "%d/%m/%Y %H:%M:%S")
        t0 = d.timestamp()
        t = t+t0
        
        x = nc.variables['mesh2d_face_x'][:]
        y = nc.variables['mesh2d_face_y'][:]
        nodes = np.zeros((len(x),2))
        nodes[:,0] = y
        nodes[:,1] = x
        
        idx = []
        poly = Polygon(np.loadtxt('polygon.csv')[:,::-1])
        for i in range(len(nodes)):
            if poly.contains(Point(nodes[i])):
                idx.append(i)
        nodes = nodes[idx]

        u = nc.variables['mesh2d_ucx'][:,:]
        u = u[:, idx]
        v = nc.variables['mesh2d_ucy'][:,:]
        v = v[:, idx]
        d = nc.variables['mesh2d_s1'][:,:]
        WD = d[:, idx]
        
        add_nodes = np.loadtxt('additional_nodes.csv')[:,::-1]
        add_u = griddata(nodes, np.transpose(u), (add_nodes), method='linear')
        add_v = griddata(nodes, np.transpose(v), (add_nodes), method='linear')
        add_WD = griddata(nodes, np.transpose(WD), (add_nodes), method='linear')
        
        add_u = np.transpose(add_u)
        add_v = np.transpose(add_v)
        add_WD = np.transpose(add_WD)
        
        u = np.concatenate((u, add_u), axis = 1)
        v = np.concatenate((v, add_v), axis = 1)
        WD = np.concatenate((WD, add_WD), axis = 1)
        nodes = np.concatenate((nodes, add_nodes))
        
        bat = np.loadtxt('E:/Use_case_Schouwen/baty_WGS.csv')[:,2]
        nodes_bat = np.loadtxt('E:/Use_case_Schouwen/baty_WGS.csv')[:,:2][:,::-1]
        bath = griddata(nodes_bat, bat, nodes, method= 'linear')       
        WD_new = np.zeros(WD.shape)
        for i in range(WD.shape[0]):
            WD_new[i] = WD[i]-bath

        WD_new[WD_new < 0] = 0
        
        self.t = t
        self.WD = WD_new
        self.u = u
        self.v = v
        self.nodes = nodes
        self.tria = Delaunay(nodes)
        self.bath = bath
        self.nodes_bat = nodes_bat
    