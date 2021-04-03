import numpy as np
import matplotlib.pyplot as plt

# Total "earth" time, one way
t_t = 3*365*24*3600
# Maximum velocity
v_max = 3e8*.999
# Acceleration 
a = 9.82

# Speed of light
c = 299792458
# time to accelerate/deccelerate
t_a = v_max/a
t_a = np.min((t_a, t_t/2))

def acc(t):
    out = np.ones_like(t)
    out[t>t_a] = 0
    out[t>(t_t-t_a)] = -1 
    out[t<0] = 0
    out[t>t_t]=0
    return a*out 

def vel(t):
    out = t_a*np.ones_like(t)
    out[t<t_a] = t[t<t_a]
    out[t>(t_t-t_a)] = t_t - t[t>(t_t-t_a)]
    out[t<0] = 0
    out[t>t_t]=0
    return a*out

def pos(t):
    p1 = t_a**2
    p2 = p1 + 2*t_a*(t_t-2*t_a)
    out = np.zeros_like(t)
    out[t<=t_a] = np.multiply(t[t<=t_a],t[t<=t_a])
    out[t>t_a] = p1 + t_a*2*(t[t>t_a]-t_a)
    ind = t>(t_t-t_a)
    out[ind] = p2 +p1 - np.flip(np.multiply(t[ind]-t_t+t_a,t[ind]-t_t+t_a))
    out[t<0] = 0
    out[t>t_t]=0
    return a*out

#https://en.wikipedia.org/wiki/Time_dilation
def time_dilation(t):
    period = 1/(t[1]-t[0])
    return period*np.cumsum(np.sqrt(1-vel(t)/c))
    
t = np.linspace(0., t_t, 1000, endpoint=True)
plt.subplot(3,1,1).plot(t, acc(t))
plt.ylabel('acceleration [m/s^2]')
plt.subplot(3,1,2).plot(t, vel(t))
plt.ylabel('velocity [m/s]')
plt.subplot(3,1,3).plot(t, pos(t))
plt.ylabel('distance [m]')
plt.xlabel('time [s]')
print(a*t_t/2)

plt.figure()

plt.subplot(2,1,1).plot(t, np.sqrt(1-vel(t)/c))
plt.ylabel('time dilation [-]')

plt.subplot(2,1,2).plot(t, time_dilation(t))
plt.ylabel('passenger time fraction')
plt.xlabel('time [s]')
    
