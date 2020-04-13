import numpy as np
import matplotlib.pyplot as plt

def learning_curve(input_filename="./progress.csv",
                   output_filename="learning_curve.png"):
    with open(input_filename, 'r') as file:
        lines = list(file)
    header = lines[0].strip().split(',')
    data = np.loadtxt(lines[1:], delimiter=',')

    if 2==data.ndim:
        plt.plot(data[:,header.index("TimestepsSoFar")],data[:,header.index("EpRewMean")])
        plt.xlabel('Timesteps')
        plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="x")
        plt.ylabel('Average Return')
        plt.ylim([-500,0])
        plt.savefig(output_filename)
        plt.close()


if __name__ == '__main__':
    learning_curve()
