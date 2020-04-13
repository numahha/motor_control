import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("step_responce.dat", delimiter=',')
plt.plot(data[:,0],data[:,1],label="input: voltage [V]")
plt.plot(data[:,0],data[:,2],label="output: angle [rad]")
plt.plot(data[:,0],data[:,3],label="angular velocity [rad/s]")

plt.xlabel('Time [sec]')
plt.xlim([-0.1, 8.1])
plt.ylim([-0.1, 13])
plt.legend()
plt.savefig("curve.png")
plt.show()

