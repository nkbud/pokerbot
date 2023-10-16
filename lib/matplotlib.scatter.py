import random

import matplotlib.pyplot as plt

if __name__ == "__main__":
    plt.axis([0,10,0,1])
    
    y = 0
    for i in range(100):
        y += random.choice([-1,1])*random.random()
        plt.scatter(i,y)
        plt.pause(0.1)
    
    plt.show()
    