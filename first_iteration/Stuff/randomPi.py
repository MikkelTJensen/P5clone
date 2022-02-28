import random
import matplotlib.pyplot as plt

x_blue = []
y_blue = []
x_red = []
y_red = []


def randomPi(number):
    partial = 0
    total = 0
    for n in range(number):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        distance = x**2 + y**2
        if distance <= 1.0:
            x_blue.append(x)
            y_blue.append(y)
            partial += 1
            total += 1
        else:
            x_red.append(x)
            y_red.append(y)
            total += 1

    return (partial/total) * 4


pi = randomPi(1000)
plt.scatter(x_red, y_red, s=1, color='red')
plt.scatter(x_blue, y_blue, s=1, color='blue', label=pi)
plt.legend(loc='upper right')
plt.show()
