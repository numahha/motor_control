import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("feedback.dat", delimiter=',')
plt.plot(data[:,2],data[:,3])

#plt.xlabel('Time [sec]')
#plt.xlim([-0.1, 8.1])
#plt.xlim([1.995, 2.005])
plt.legend()
plt.savefig("phase.png")
plt.show()

