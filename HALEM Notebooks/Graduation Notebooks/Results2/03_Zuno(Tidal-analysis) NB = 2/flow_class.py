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

class flow_tidal_analysis():
    def __init__(self):

        nodes = np.loadtxt('D:/Use_case_Schouwen/tidal_an/nodes.csv')
        print('Loading 20 %')
        t = np.loadtxt('D:/Use_case_Schouwen/tidal_an/t.csv')
        clear_output(wait= True)
        print('Loading 40 %')
        WD = np.loadtxt('D:/Use_case_Schouwen/tidal_an/d.csv')
        clear_output(wait= True)
        print('Loading 60 %')
        u = np.loadtxt('D:/Use_case_Schouwen/tidal_an/u.csv')
        clear_output(wait= True)
        print('Loading 80 %')
        v = np.loadtxt('D:/Use_case_Schouwen/tidal_an/v.csv')
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

        a = 47
        b = 361
        time_orig = (t)/60/60/24
        time = time_orig[::6][a:(a+b)]

        WD_t = np.zeros((len(time), len(nodes)))
        u_t = np.zeros((len(time), len(nodes)))
        v_t = np.zeros((len(time), len(nodes)))
        
        Rayleigh_min = 2.3
        q = int(0)
        qq = 1
        for node in range(len(nodes)):
            q = q + int(1)
            if q == 10:
                clear_output(wait= True)
                print(np.round(qq/ len(nodes)*1000,3), '%')
                q = int(0)
                qq +=1
            WD_raw = WD[:,node]
            u_raw = u[:,node]
            v_raw = v[:,node]
            WD_predict, u_predict, v_predict = self.Tidal_analysis(time_orig, time, WD_raw, u_raw, v_raw, Rayleigh_min)
            WD_t[:,node] = WD_predict['h']
            u_t[:,node] = u_predict['h']
            v_t[:,node] = v_predict['h']
        
        print(WD_t.shape)
        WD_new = np.zeros(WD_t.shape)
        for i in range(WD_t.shape[0]):
            WD_new[i] = WD_t[i]-bath

        WD_new[WD_new < 0] = 0

        t = np.loadtxt('D:/Use_case_Schouwen/tidal_an/t.csv')
        a = 47
        b = 361
        t = (t)[::6][a:(a+b)]

        self.t = t
        self.WD = WD_new
        self.u = u_t
        self.v = v_t
        self.nodes = nodes
        self.tria = Delaunay(nodes)
        # self.bath = bath
        # self.WD_t = WD_t
    
    def Tidal_analysis(self, time_orig, time, WD_raw, u_raw, v_raw, Rayleigh_min):
        coef_WD = utide.solve(time_orig, WD_raw,
                            lat=53,
                            nodal=False,
                            trend=False,
                            method='ols',
                            conf_int='linear',
                            Rayleigh_min=Rayleigh_min,)

        WD_predict = utide.reconstruct(time, coef_WD)


        coef_u = utide.solve(time_orig, u_raw,
                            lat=53,
                            nodal=False,
                            trend=False,
                            method='ols',
                            conf_int='linear',
                            Rayleigh_min=Rayleigh_min,)

        u_predict = utide.reconstruct(time, coef_u)

        coef_v = utide.solve(time_orig, v_raw,
                            lat=53,
                            nodal=False,
                            trend=False,
                            method='ols',
                            conf_int='linear',
                            Rayleigh_min=Rayleigh_min,)

        v_predict = utide.reconstruct(time, coef_v)
        
        
        clear_output()
        return WD_predict, u_predict, v_predict

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