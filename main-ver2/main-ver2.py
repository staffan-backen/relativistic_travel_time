import numpy as np
import scipy.constants as spc
import matplotlib.pyplot as plt

# alpha = c^2*dgamma/dx
# dx_AB = distance
# Midpoint lorentz factor
# gamma_mid = 1 + alpha*(dx_AB/2)/c^2 
# Round trip time traveler
# dtau = 4*(c/alpha)*arccosh(gamma_mid)
# Round trip earth
# dt = 4*c/alpha*sinh(arccosh(gamma_mid))

# Objects in the universe
objects = {"Moon": 238900*spc.mile, 
           "Mars": 167.02e6*spc.mile, 
           "1AU (Sun)":spc.au, 
           "Jupiter": 524.42e6*spc.mile,
           "Interstellar space": 121*spc.au,
           "light year":spc.light_year, 
           "Kepler-22b (<great exo)":620*spc.light_year,
           "Proxima Centauri (<Star)":4.2465*spc.light_year, 
           "V616 Monocerotis (<Black hole)":3500*spc.light_year,
           "Pillars of Creation": 6750*spc.light_year,
           "Sagittarius A (Milky Way center)":25e3*spc.light_year, 
           "Andromeda (<Galaxy)":2.5e6*spc.light_year,
           "Visible Universe":4.4e26}

def time_convenient(t):
    if t < spc.hour:
        return "{0:.2f} s".format(t)
    if t < spc.day:
        return "{0:.2f} hours".format(t/spc.hour)
    if t < spc.year:
        return "{0:.2f} days".format(t/spc.day)
    k = int(np.floor(np.log10(t/spc.year)/3))
    str = "kMGTPE"
    if k > 5:
        k = 5
    prefix = str[k]
    factor = 10**(3*k)
    return "{0:.4f} {1:s}y".format(t/spc.year/factor, prefix)

  class RelativisticTravelTimes:
    # https://en.wikipedia.org/wiki/Proper_acceleration#Acceleration in (1+1)D
    def __init__(self, g_force, distance):
        self.acceleration = g_force*9.8 
        self.distance = distance
        self.gamma_mid = 1+self.acceleration*(self.distance/2.)/spc.c**2
        
    def time_traveler(self):
        return 4.*spc.c/self.acceleration*np.arccosh(self.gamma_mid)

    def time_earth(self):
        return 4.*(spc.c/self.acceleration)*np.sinh(np.arccosh(self.gamma_mid))
    
    def max_speed(self):
        # gamma = 1/(sqrt(1-v^2/c^2)) -> 1-v^2/c^2 = 1/gamma^2 -> v = sqrt((1+1/gamma^2)*c^2)
        return np.sqrt((1+1/self.gamma_mid**2)*spc.c**2)    
    
    def __str__(self):
        return "Traveler: {0:>12s}, Earth: {1:>12s}, f_max_c: {2:.15f}".format(
                time_convenient(self.time_traveler()), 
                time_convenient(self.time_earth()), 
                spc.c/self.max_speed())
    
    
    
for key in objects.keys():
    print("{0:35s}".format(key), "|", RelativisticTravelTimes(1, objects[key]))

fig = plt.figure()
ax = fig.add_subplot()
print(np.min(list(objects.values())))
print(np.max(list(objects.values())))
distances = np.geomspace(1e8, 1e26,100)
for acceleration in np.power(2.,range(0,4)): #[0.0625, 0.125, .25, .5, 1, 2, 4, 8, 16]:
    t_pairs = []
    for distance in distances:
        rtt = RelativisticTravelTimes(acceleration, distance)
        t_pairs.append([rtt.time_traveler(), rtt.time_earth()])
    vecs = np.array(t_pairs).T 
    ax.plot((vecs[0])/spc.year, (vecs[1])/spc.year,"x-")
ax.set_xlabel("$t_{traveler}$")
ax.set_ylabel("$t_{earth}$")

  
