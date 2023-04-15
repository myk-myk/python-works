import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import math

def points_input(input_type, point_list=None):
    if input_type and point_list is None:
        points, name = [], {}
        point_count = int(input("Кількість точок: "))
        print("Введіть точки: ")
        for j in range(point_count):
            points.append([int(value) for value in input().split()])
        x, y, count = [], [], 1
        for point in points:
            point_name = "X" + str(count)
            name.update({point_name: list(map(int, point))})
            count += 1
            x.append(point[0])
            y.append(point[1])
        x, y = np.array(x), np.array(y)
        return x, y, name
    elif not input_type and point_list is None:
        points_file = open("points.txt", "r")
        points, name = points_file.readlines(), {}
        x, y, count = [], [], 1
        for point in points:
            point = point.replace("\n", '')
            point = point.split(' ')
            point_name = "X" + str(count)
            name.update({point_name: list(map(int, point))})
            count += 1
            x.append(int(point[0]))
            y.append(int(point[1]))
        x, y = np.array(x), np.array(y)
        return x, y, name
    elif point_list is not None:
        x, y = [], []
        for point in point_list:
            x.append(point[0])
            y.append(point[1])
        x, y = np.array(x), np.array(y)
        return x, y

def maxmin_algorithm(x_range, y_range):
    clusters, points = [], []
    for y, x in enumerate(x_range):
        temp = [x, y_range[y]]
        points.append(temp)
    points_distance, clust_centers, centers_l = [], {}, []
    points_not_centers = points.copy()
    if points:
        clust_centers.update({f"Z{len(clust_centers) + 1}": points[0]})
    points_not_centers.remove(points[0])
    for clust_center in list(clust_centers.values()):
        for point in points_not_centers:
            dist = 0
            for i in range(len(point)):
                dist += pow(point[i] - clust_center[i], 2)
            dist = math.sqrt(dist)
            points_distance.append(dist)
    max_dist, max_dist_index = max(points_distance), points_distance.index(max(points_distance))
    li, l = max_dist, max_dist
    while li > l / 2:
        clust_centers.update({f"Z{len(clust_centers) + 1}": points_not_centers[max_dist_index]})
        points_not_centers.remove(points_not_centers[max_dist_index])
        centers_l.append(max_dist)
        l = 0
        for center_l in centers_l:
            l += center_l
        l = l / len(centers_l)
        points_distance = []
        for point in points_not_centers:
            distance = []
            for clust_center in list(clust_centers.values()):
                dist = 0
                for i in range(len(point)):
                    dist += pow(point[i] - clust_center[i], 2)
                dist = math.sqrt(dist)
                distance.append(dist)
            points_distance.append(min(distance))
        max_dist, max_dist_index = max(points_distance), points_distance.index(max(points_distance))
        li = max_dist
    for clust_center in list(clust_centers.values()):
        clust = []
        clust.append(clust_center)
        clusters.append(clust)
    for point in points_not_centers:
        distance = []
        for clust_center in list(clust_centers.values()):
            dist = 0
            for i in range(len(point)):
                dist += pow(point[i] - clust_center[i], 2)
            dist = math.sqrt(dist)
            distance.append(dist)
        min_dist, min_dist_index = min(distance), distance.index(min(distance))
        clusters[min_dist_index].append(point)
    return clusters, clust_centers

def k_means(num_clusters, x_range, y_range, center_choise):
    clusters, points = [], []
    for y, x in enumerate(x_range):
        temp = [x, y_range[y]]
        points.append(temp)
    if not center_choise:
        clust_centers = {}
        if len(points) >= num_clusters:
            for i in range(0, num_clusters):
                clust_centers.update({f"Z{len(clust_centers) + 1}": points[i]})
    else:
        _, clust_centers = maxmin_algorithm(x_range, y_range)
    finish_accuracy, finish_condition = 0.1, False
    while finish_condition is False:
        clusters = []
        for i in range(0, num_clusters):
            clusters.append([])
        for point in points:
            distance = []
            for clust_center in list(clust_centers.values()):
                dist = 0
                for i in range(len(point)):
                    dist += pow(point[i] - clust_center[i], 2)
                dist = math.sqrt(dist)
                distance.append(dist)
            min_dist, min_dist_index = min(distance), distance.index(min(distance))
            clusters[min_dist_index].append(point)
        new_clust_centers = {}
        for cluster_val in clusters:
            x, y = 0, 0
            for point in cluster_val:
                x += point[0]
                y += point[1]
            x = x / len(cluster_val)
            y = y / len(cluster_val)
            new_clust_center = [x, y]
            new_clust_centers.update({f"Z{len(new_clust_centers) + 1}": new_clust_center})
        centers_diff = []
        for count, clust_center in enumerate(list(clust_centers.values())):
            diff = 0
            for i in range(len(clust_center)):
                diff += pow(clust_center[i] - list(new_clust_centers.values())[count][i], 2)
            diff = math.sqrt(diff)
            centers_diff.append(diff)
        clust_centers = new_clust_centers.copy()
        for center_diff in centers_diff:
            if center_diff < finish_accuracy:
                finish_condition = True
            else:
                finish_condition = False
                break
    return clusters, clust_centers

if __name__ == '__main__':
    x_axis, y_axis, points_name = points_input(False)
    cluster_count = int(input("Кількість кластерів: "))
    plt.plot(x_axis, y_axis, 'o')
    plt.title("Вхідні дані")
    plt.xlabel("x")
    plt.ylabel("y")
    for j in range(len(x_axis)):
        cluster_point = [x_axis[j], y_axis[j]]
        plt.annotate(list(points_name.keys())[list(points_name.values()).index(cluster_point)], (x_axis[j], y_axis[j]))
    plt.grid()
    plt.show()
    cluster, clusters_center = k_means(cluster_count, x_axis, y_axis, True)
    center_x, center_y = points_input(True, list(clusters_center.values()))
    print(f"Алгоритм виділив {len(cluster)} кластери:")
    for num, clust in enumerate(cluster):
        print(f"{num + 1} кластер - ", end="")
        for point_val in clust:
            print(f"{list(points_name.keys())[list(points_name.values()).index(point_val)]}: {point_val} ", end="")
        print()
        cl_x, cl_y = points_input(True, clust)
        plt.scatter(cl_x, cl_y)
        for j in range(len(cl_x)):
            cluster_point = [cl_x[j], cl_y[j]]
            plt.annotate(list(points_name.keys())[list(points_name.values()).index(cluster_point)],
                             (cl_x[j], cl_y[j]))
    plt.scatter(center_x, center_y, color="black")
    for j in range(len(center_x)):
        center_point = [center_x[j], center_y[j]]
        plt.annotate(list(clusters_center.keys())[list(clusters_center.values()).index(center_point)],
                     (center_x[j], center_y[j]))
    print("Центри кластерів:", clusters_center)
    plt.title("Виділені кластери")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.show()
