import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import copy

def points_input(input_type, point_list=None):
    if input_type and point_list is None:
        name, classes, count = {}, [], 1
        class_count = int(input(f"Кількість класів: "))
        for i in range(class_count):
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

def perceptron_classes(class_points):
    c, w = 1, []
    for j in range(len(class_points)):
        w.append([0, 0, 0])
    cl_points = copy.deepcopy(class_points)
    for cl in cl_points:
        for point in cl:
            point.append(1)
    change = True
    while change is True:
        iter_change = []
        for ind, cl in enumerate(cl_points):
            for point in cl:
                classification = {}
                for j, wi in enumerate(w):
                    classific = multiply_matrix(wi, point)
                    classific = classific[0][0]
                    classification.update({j: classific})
                classification = dict(sorted(classification.items(), key=lambda item: item[1], reverse=True))
                if list(classification.keys())[0] == ind and list(classification.values())[0] > list(classification.values())[1]:
                    iter_change.append(False)
                else:
                    cx = list_on_int(c, point)
                    w[ind] = sum_list(w[ind], cx)
                    curr_class = classification.pop(ind)
                    for j, clas in enumerate(list(classification.values())):
                        if curr_class <= clas:
                            w[list(classification.keys())[j]] = subtract_list(w[list(classification.keys())[j]], cx)
                            iter_change.append(True)
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
    plt.legend(loc="lower left")
    plt.grid()
    plt.show()
    function_indexes = perceptron_classes(class_values)
    print("Вагові вектори:")
    for i, index in enumerate(function_indexes):
        print(f"w{i + 1} = {index[0]}x + ({index[1]}y) + ({index[2]})")
        lrf_x, lrf_y = function(index)
        plt.plot(lrf_x, lrf_y)
    text_y = len(function_indexes)
    for i, function in enumerate(function_indexes):
        plt.text(1.3, text_y, f"w{i + 1} = {function[0]}x + ({function[1]}y) + ({function[2]})")
        text_y -= 1
    for i, cl in enumerate(classes):
        class_values.append(list(cl.values()))
        cl_x, cl_y = points_input(True, list(cl.values()))
        plt.scatter(cl_x, cl_y, label=f"A{i + 1}")
        for j in range(len(cl_x)):
            class_point = [cl_x[j], cl_y[j]]
            plt.annotate(list(cl.keys())[list(cl.values()).index(class_point)],
                         (cl_x[j], cl_y[j]))
    plt.title("Лінійні рішаючі функції")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc="upper left")
    plt.grid()
    plt.show()
