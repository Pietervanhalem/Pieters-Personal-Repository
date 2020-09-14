import numpy as np
from IPython.display import clear_output  
    
class ConvectionDiffussion:    
    def __init__(
        self, 
        flow,
        initial_conditions,
        K = 0.282,
        dt = 0.5,
        dx = 1,
        dy = 1,
        L = 100,
        B = 100,
        T = 300
    ):        
        # Diffusion cooficent source: https://en.wikipedia.org/wiki/Mass_diffusivity
        self.K = K
        
        self.dt = dt
        self.dx = dx
        self.dy = dy
        
        self.L = L
        self.B = B
        self.T = T
        
        x = np.arange(0, self.L, self.dx)
        y = np.arange(0, self.B, self.dy)
        t = np.arange(0, self.T, self.dt)
        self.x,self.t,self.y = np.meshgrid(x,t, y)
        
        self.u, self.v = flow(self.x, self.y, self.t)
        self.c = initial_conditions(self.x, self.y, self.t)
                
        u_bar = (self.u **2 + self.v**2) ** 0.5
        print(f"q = {self.K *self.dt/(self.dx**2)} < 1/2")
        print(f"P_Delta = {u_bar.max() * self.dx / self.K } < 2")
        
   
    def Kdcdx2(self, t, x, y):
        return self.K * (self.c[t-1,x-1,y] - 2 * self.c[t-1,x,y] + self.c[t-1,x+1,y])/(self.dx ** 2)
    
    def Kdcdy2(self, t, x, y):
        return self.K * (self.c[t-1,x,y-1] - 2 * self.c[t-1,x,y] + self.c[t-1,x,y+1])/(self.dy ** 2)
    
    def vdcdx(self, t, x, y):
        return self.u[t-1,x,y] * (self.c[t-1,x+1,y] - self.c[t-1,x-1,y])/ (2 * self.dx)
    
    def udcdy(self, t, x, y):
        return self.v[t-1,x,y] * (self.c[t-1,x,y+1] - self.c[t-1,x,y-1])/ (2 * self.dy)
    
    def run(self):
        for k in range(1, self.c.shape[0]):
            clear_output(True)
            print(f"{np.round(k/self.c.shape[0] * 100, 2)} %")
            
            for i in range(1, self.c.shape[1]-1):
                for j in range(1, self.c.shape[2]-1):      
                    new_c = self.c[k-1,i,j] + self.dt * (
                        self.Kdcdx2(k,i,j)+
                        self.Kdcdy2(k,i,j)-
                        self.udcdy(k,i,j)-
                        self.vdcdx(k,i,j)
                    )
                    self.c[k,i,j] = new_c