import numpy as np
import datetime, time
from datetime import datetime
import pickle
import halem
import datetime, time
import numpy as np
timeQ = time
from pandas import DataFrame
from scipy.spatial import Delaunay
from IPython.display import clear_output
from scipy.interpolate import griddata
import utide
from pandas import date_range
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class flow_tidal_real():
    def __init__(self):
        nodes = np.loadtxt('D:/Use_case_Schouwen/Zuno_data/CSV/nodes.csv')
        print('Loading 20 %')
        t = np.loadtxt('D:/Use_case_Schouwen/Zuno_data/CSV/t.csv')
        clear_output(wait= True)
        print('Loading 40 %')
        WD = np.loadtxt('D:/Use_case_Schouwen/Zuno_data/CSV/d.csv')
        clear_output(wait= True)
        print('Loading 60 %')
        u = np.loadtxt('D:/Use_case_Schouwen/Zuno_data/CSV/u.csv')
        clear_output(wait= True)
        print('Loading 80 %')
        v = np.loadtxt('D:/Use_case_Schouwen/Zuno_data/CSV/v.csv')
        clear_output(wait= True)
        print('loading 100 %')

        add_nodes = np.loadtxt('additional_nodes.csv')[:,::-1]

        add_u = griddata(nodes, np.transpose(u), (add_nodes), method='linear')
        print('interpolating 1/3')
        add_v = griddata(nodes, np.transpose(v), (add_nodes), method='linear')
        print('interpolating 1/3')
        add_WD = griddata(nodes, np.transpose(WD), (add_nodes), method='linear')
        print('interpolating 1/3')

        add_u = np.transpose(add_u)
        add_v = np.transpose(add_v)
        add_WD = np.transpose(add_WD)

        u = np.concatenate((u, add_u), axis = 1)
        v = np.concatenate((v, add_v), axis = 1)
        WD = np.concatenate((WD, add_WD), axis = 1)
        nodes = np.concatenate((nodes, add_nodes))

        bat = np.loadtxt('D:/Use_case_Schouwen/baty_WGS.csv')[:,2]
        nodes_bat = np.loadtxt('D:/Use_case_Schouwen/baty_WGS.csv')[:,:2][:,::-1]

        bath = griddata(nodes_bat, bat, nodes, method= 'cubic')


        WD_new = np.zeros(WD.shape)
        for i in range(WD.shape[0]):
            WD_new[i] = WD[i]-bath

        WD_new[WD_new < 0] = 0

        t = np.loadtxt('D:/Use_case_Schouwen/Zuno_data/CSV/t.csv')

        WD = WD_new[::6,:]
        u = u[::6,:]
        v = v[::6,:]
        t = t[::6]

        idx = []
        poly = Polygon(np.loadtxt('polygon.csv')[:,::-1])
        for i in range(len(nodes)):
            if poly.contains(Point(nodes[i])):
                idx.append(i)
                
        len(idx)

        nodes = nodes[idx]
        WD = WD[:, idx]
        u = u[:, idx]
        v = v[:, idx]


        self.t = t
        self.WD = WD
        self.u = u
        self.v = v
        self.nodes = nodes
        self.tria = Delaunay(nodes)
   

class flow_tides():
    def __init__(self, name):
        with open(name, 'rb') as input:
            flow = pickle.load(input)

        self.t = flow.t
        self.WD = flow.WD
        self.u = flow.u
        self.v = flow.v
        self.nodes = flow.nodes
        self.tria = flow.tria