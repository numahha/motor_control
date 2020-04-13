import numpy as np
import matplotlib.pyplot as plt

# This scripts is only for pendulum.

def phase_portrait(input_filename="./real_world_samples_input_2.csv",
                   output_filename="./phase.png"):
    data = np.loadtxt(input_filename, delimiter=',')

    plt.plot(data[:,0],data[:,1])
    plt.xlabel('Angle')
    #plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="x")
    plt.ylabel('Angler Velocity')
    plt.savefig(output_filename)
    plt.close()


if __name__ == '__main__':
    phase_portrait()
