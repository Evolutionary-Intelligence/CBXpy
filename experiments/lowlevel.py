import numpy as np
import cbx as cbx
from cbx.dynamic import CBO
from cbx.objectives import Rastrigin
from cbx.utils.objective_handling import batched_objective
from cbx.utils.scheduler import scheduler, multiply

np.random.seed(42)
#%%
conf = {'alpha': 100.0,
        'dt': 0.01,
        'sigma': 6.0,
        'lamda': 1.0,
        'batch_size':100,
        'd': 20,
        'max_it': 5000,
        'N': 100,
        'M': 2}

#%% Define the objective function
mode = 'import'
if mode == 'import':
    f = Rastrigin()
else:
    @batched_objective
    def f(x):
        return np.linalg.norm(x, axis=-1)

#%% Define the initial positions of the particles
x = cbx.utils.init_particles(shape=(conf['M'], conf['N'], conf['d']), x_min=-3., x_max = 3.)

#%% Define the CBO algorithm
dyn = CBO(f, x=x, noise='anisotropic', f_dim='2D', 
          **conf)
sched = scheduler(dyn, [multiply(name='alpha', factor=1.1, maximum=1e15),
                        #multiply(name='sigma', factor=1.005, maximum=6.)
                        ])
#%% Run the CBO algorithm
t = 0
it = 0
while not dyn.terminate():
    dyn.step()
    sched.update()
    
    if it%10 == 0:
        print(dyn.f_min)
        print('Alpha: ' + str(dyn.alpha))
        print('Sigma: ' + str(dyn.sigma))
        
    it+=1