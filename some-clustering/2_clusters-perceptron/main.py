import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import copy

def points_input(input_type, point_list=None):
    if input_type and point_list is None:
        name, classes, count = {}, [], 1
        for i in range(2):
            points = []
            point_count = int(input(f"Кількість точок в {i + 1} класі: "))
            print("Введіть точки: ")
            for j in range(point_count):
                points.append([int(value) for value in input().split()])
            for point in points:
                point_name = "X" + str(count)
                name.update({point_name: list(map(int, point))})
                count += 1
            classes.append(name)
            name = {}
        return classes
    elif not input_type and point_list is None:
        points_file = open("points.txt", "r")
        points, name = points_file.readlines(), {}
        count = 1
        classes = []
        for point in points:
            if point != '\n':
                point = point.replace("\n", '')
                point = point.split(' ')
                point_name = "X" + str(count)
                name.update({point_name: list(map(int, point))})
                count += 1
            else:
                classes.append(name)
                name = {}
        classes.append(name)
        return classes
    elif point_list is not None:
        x, y = [], []
        for point in point_list:
            x.append(point[0])
            y.append(point[1])
        x, y = np.array(x), np.array(y)
        return x, y

def sum_list(w_coef, x_column):
    result_list = []
    for ind in range(len(w_coef)):
        result_list.append(w_coef[ind] + x_column[ind])
    return result_list

def subtract_list(w_coef, x_column):
    result_list = []
    for ind in range(len(w_coef)):
        result_list.append(w_coef[ind] - x_column[ind])
    return result_list

def list_on_int(value, point_list):
    result_list = []
    for val in point_list:
        result_list.append(val * value)
    return result_list

def multiply_matrix(w_coef, x_column):
    result = []
    column = []
    coef = [w_coef]
    for val in x_column:
        row = [val]
        column.append(row)
    for i in range(len(coef)):
        row = []
        for j in range(len(column[0])):
            value = 0
            for k in range(len(column)):
                value += coef[i][k] * column[k][j]
            row.append(value)
        result.append(row)
    return result

def perceptron_2class(class_points):
    c, w = 1, [0, 0, 0]
    cl_points = copy.deepcopy(class_points)
    for cl in cl_points:
        for point in cl:
            point.append(1)
    change = True
    while change is True:
        iter_change = []
        for ind, cl in enumerate(cl_points):
            for point in cl:
                classification = multiply_matrix(w, point)
                classification = classification[0][0]
                if ind == 0:
                    if classification <= 0:
                        cx = list_on_int(c, point)
                        w = sum_list(w, cx)
                        iter_change.append(True)
                    else:
                        iter_change.append(False)
                elif ind == 1:
                    if classification >= 0:
                        cx = list_on_int(c, point)
                        w = subtract_list(w, cx)
                        iter_change.append(True)
                    else:
                        iter_change.append(False)
        for change_val in iter_change:
            if not change_val:
                change = False
            else:
                change = True
                break
    return w

def function(w):
    x = np.linspace(-2, 8, 100)
    y = w[0] * x + w[2]
    y = y / (-w[1] + 1)
    return x, y

if __name__ == '__main__':
    classes = points_input(False)
    class_values = []
    print("Вхідні дані (класи):")
    for clas in classes:
        print(clas)
    for i, cl in enumerate(classes):
        class_values.append(list(cl.values()))
        cl_x, cl_y = points_input(True, list(cl.values()))
        plt.scatter(cl_x, cl_y, label=f"A{i + 1}")
        for j in range(len(cl_x)):
            class_point = [cl_x[j], cl_y[j]]
            plt.annotate(list(cl.keys())[list(cl.values()).index(class_point)],
                         (cl_x[j], cl_y[j]))
    plt.title("Вхідні дані")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc="upper left")
    plt.grid()
    plt.show()
    function_indexes = perceptron_2class(class_values)
    lrf_x, lrf_y = function(function_indexes)
    print("Ваговий вектор:", f"w = {function_indexes[0]}x + ({function_indexes[1]}y) + ({function_indexes[2]})")
    plt.plot(lrf_x, lrf_y)
    plt.text(1.3, 1, f"w = {function_indexes[0]}x + ({function_indexes[1]}y) + ({function_indexes[2]})")
    for i, cl in enumerate(classes):
        class_values.append(list(cl.values()))
        cl_x, cl_y = points_input(True, list(cl.values()))
        plt.scatter(cl_x, cl_y, label=f"A{i + 1}")
        for j in range(len(cl_x)):
            class_point = [cl_x[j], cl_y[j]]
            plt.annotate(list(cl.keys())[list(cl.values()).index(class_point)],
                         (cl_x[j], cl_y[j]))
    plt.title("Лінійна рішаюча функція")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc="upper left")
    plt.grid()
    plt.show()
