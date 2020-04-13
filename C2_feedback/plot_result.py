import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("feedback.dat", delimiter=',')
plt.plot(data[:,0],data[:,1],label="input: voltage [V]")
plt.plot(data[:,0],data[:,2],label="output: angle [rad]")

import copy
velocity = copy.copy(data[:,2])
print(velocity.shape[0])

velocity[0]=0.
velocity[1]=0.
for i in range(2,velocity.shape[0]):
    velocity[i] = (data[i,2]- data[i-1,2])/(data[1,0]- data[0,0])
    velocity[i] = (velocity[i] + velocity[i-1])/2.

plt.plot(data[:,0],velocity,label="angular velocity [rad/s]")

plt.xlabel('Time [sec]')
plt.xlim([-0.1, 8.1])
#plt.xlim([1.995, 2.005])
plt.legend()
plt.savefig("curve.png")
plt.show()

