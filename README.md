# NLsimulation
Model with simulation of a sculpture I made out of photosensitive night lights.
Night Light Simulation Version 2 
(Version 1 created a 100 x 100 x 100 numpy array to store values 
for the intensity at every point in the space. This is unnecessary since the only relevant points 
in the simualtion are the 200-400 {out of 1,000,000!} where objects are positioned!)
    
Gist of model:
Environment created by randomly positioning objects (from a uniform discrete distribution),and 
initializing object parameters from the normal distribution given the model parameters.
Each iteration calculates the 'local' intensity at every object position and changes the state 
according to the sensitivity of the object. 
The simulation is not deterministic since each object's brightness is randomly generated at
each iteration. 
