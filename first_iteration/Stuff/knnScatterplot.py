import matplotlib.pyplot as plt


picture = 2

if picture == 1:
    x_blue = [3, 2, 4, 3, 2, 3]
    y_blue = [1, 2, 2, 3, 4, 5]
    x_red = [4]
    y_red = [7]
    x_green = [7, 5, 6, 5, 8, 7]
    y_green = [7, 8, 8, 9, 9, 10]

    plt.scatter(x_red, y_red, s=20, color='orange', label='New Point')
    plt.scatter(x_blue, y_blue, s=20, color='red', label='Category A')
    plt.scatter(x_green, y_green, s=20, color='blue', label='Category B')
    plt.rcParams['legend.handlelength'] = 0
    plt.legend(loc='lower right')
    plt.show()
elif picture == 2:
    x_dot = [3]
    y_dot = [9]
    x_dots = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    y_dots = []
    for x in x_dots:
        y_dots.append(x**2)

    plt.plot(x_dots, y_dots)
    plt.scatter(x_dot, y_dot, s=20, color='red', label='X Value')
    plt.axvline(x=0.0, color='black')
    plt.axhline(y=0.0, color='black')
    plt.grid(True)
    plt.rcParams['legend.handlelength'] = 0
    plt.legend(loc='lower right')
    plt.show()
