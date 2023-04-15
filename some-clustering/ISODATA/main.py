import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import math
import itertools

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

def krok1(thetaN, thetaS, thetaC, L, Nc):
    return thetaN, thetaS, thetaC, L, Nc

def krok2(cluster_centers, points):
    clusters = []
    for i in range(0, len(cluster_centers)):
        clusters.append([])
    for point in points:
        distance = []
        for clust_center in list(cluster_centers.values()):
            dist = 0
            for i in range(len(point)):
                dist += pow(point[i] - clust_center[i], 2)
            dist = math.sqrt(dist)
            distance.append(dist)
        min_dist, min_dist_index = min(distance), distance.index(min(distance))
        clusters[min_dist_index].append(point)
    Ni = []
    for clust in clusters:
        Ni.append(len(clust))
    Nc = len(clusters)
    return clusters, Ni, Nc

def krok3(clusters, cluster_centers, points, Ni, thetaN):
    Nc, points_count = len(clusters), len(points)
    for i, N in enumerate(Ni):
        if N < thetaN:
            Ni.pop(i)
            delete_clust = clusters.pop(clusters.index(clusters[i]))
            cluster_centers.pop(list(cluster_centers.keys())[i])
            for point in delete_clust:
                points.remove(point)
            Nc = len(clusters)
            points_count = len(points)
    return clusters, cluster_centers, points, Ni, Nc, points_count

def krok4(clusters):
    cluster_centers = {}
    for i, cluster_val in enumerate(clusters):
        x, y = 0, 0
        for point in cluster_val:
            x += point[0]
            y += point[1]
        x = x / len(cluster_val)
        y = y / len(cluster_val)
        clust_center = [x, y]
        cluster_centers.update({f"Z{len(cluster_centers) + 1}": clust_center})
    return cluster_centers

def krok5(clusters, cluster_centers, points):
    cluster_distance, points_distance = [], []
    for i, cluster_val in enumerate(clusters):
        distance = []
        for point in points:
            if cluster_val.__contains__(point):
                dist = 0
                for j in range(len(point)):
                    dist += pow(point[j] - list(cluster_centers.values())[i][j], 2)
                dist = math.sqrt(dist)
                distance.append(dist)
        points_distance.append(distance)
    for clust_distance in points_distance:
        clust_dist = 0
        for dist_val in clust_distance:
            clust_dist += dist_val
        clust_dist = clust_dist / len(clust_distance)
        cluster_distance.append(clust_dist)
    return cluster_distance

def krok6(cluster_distance, Ni, points_count):
    aver_distance = 0
    for i, distance in enumerate(cluster_distance):
        aver_distance += distance * Ni[i]
    aver_distance = aver_distance / points_count
    return aver_distance

def krok8(clusters, cluster_centers, Ni):
    aver_deviation = []
    for i, cluster_val in enumerate(clusters):
        x, y = [], []
        for point in cluster_val:
            x.append(point[0])
            y.append(point[1])
        x_sigma, y_sigma = 0, 0
        for j in range(0, len(x)):
            x_sigma += pow(x[j] - list(cluster_centers.values())[i][0], 2)
            y_sigma += pow(y[j] - list(cluster_centers.values())[i][1], 2)
        x_sigma, y_sigma = x_sigma / Ni[i], y_sigma / Ni[i]
        x_sigma, y_sigma = math.sqrt(x_sigma), math.sqrt(y_sigma)
        sigma = [x_sigma, y_sigma]
        aver_deviation.append(sigma)
    return aver_deviation

def krok9(aver_deviation):
    max_deviation, max_deviation_index = [], []
    for deviation in aver_deviation:
        max_dev, max_dev_index = max(deviation), deviation.index(max(deviation))
        max_deviation.append(max_dev)
        max_deviation_index.append(max_dev_index)
    return max_deviation, max_deviation_index

def krok10(clust_centers, max_deviation, max_deviation_index, thetaS, Nc, K, cluster_distance, average_distance, thetaN, Ni):
    cluster_centers_change, new_cluster_centers, dev_status = [], [], False
    for j, deviation in enumerate(max_deviation):
        if deviation > thetaS and ((Nc <= K / 2) or (cluster_distance[j] > average_distance and Ni[j] > 2 * (thetaN + 1))):
            gamma, dev_status = 0.5 * deviation, True
            new_clust_center_min = list(clust_centers.values())[j][max_deviation_index[j]] - gamma
            new_clust_center_max = list(clust_centers.values())[j][max_deviation_index[j]] + gamma
            new_min_clust_center, new_max_clust_center = list(clust_centers.values())[j].copy(), list(clust_centers.values())[j].copy()
            new_min_clust_center[max_deviation_index[j]] = new_clust_center_min
            new_max_clust_center[max_deviation_index[j]] = new_clust_center_max
            cluster_centers_change.append(list(clust_centers.values())[j])
            new_cluster_centers.append(new_max_clust_center)
            new_cluster_centers.append(new_min_clust_center)
            Nc += 1
    cluster_centers = list(clust_centers.values())
    for clust in cluster_centers:
        if cluster_centers_change.__contains__(clust):
            clust_index = cluster_centers.index(clust)
            cluster_centers = cluster_centers[:clust_index] + [new_cluster_centers.pop(0)] + [new_cluster_centers.pop(0)] + cluster_centers[clust_index + 1:]
    clust_centers = {}
    for clust in cluster_centers:
        clust_centers.update({f"Z{len(clust_centers) + 1}": clust})
    Nc = len(clust_centers)
    return clust_centers, Nc, dev_status

def krok11(cluster_centers):
    center_combinations = list(itertools.combinations(list(cluster_centers.values()), 2))
    center_indexes = []
    for clust_center in list(cluster_centers.values()):
        center_indexes.append(list(cluster_centers.values()).index(clust_center))
    center_indexes_comb = list(itertools.combinations(center_indexes, 2))
    center_distance = []
    for center_comb in center_combinations:
        dist = 0
        for j in range(len(center_comb)):
            dist += pow(center_comb[0][j] - center_comb[1][j], 2)
        dist = math.sqrt(dist)
        center_distance.append(dist)
    return center_distance, center_indexes_comb

def krok12(center_distance, center_indexes, thetaC, L):
    low_distance = {}
    for i, center_dist in enumerate(center_distance):
        if center_dist < thetaC:
            if len(low_distance) <= L:
                low_distance.update({center_indexes[i]: center_dist})
    low_distance = dict(sorted(low_distance.items(), key=lambda indexes: indexes[1]))
    return low_distance

def krok13(cluster_centers, low_distance, Ni, Nc):
    if len(low_distance) > 0:
        new_centers, centers_delete, distance_delete = [], [], []
        for i, indexes in enumerate(list(low_distance.keys())):
            centers, new_center, cl_points_count = [], [], []
            for ind in indexes:
                centers.append(list(cluster_centers.values())[ind])
                distance_delete.append(ind)
                cl_points_count.append(Ni[ind])
            centers_delete += centers.copy()
            for j in range(len(centers)):
                coordinate = cl_points_count[0] * centers[0][j] + cl_points_count[1] * centers[1][j]
                coordinate = coordinate / (sum(cl_points_count))
                new_center.append(coordinate)
            new_centers.append(new_center)
            Nc -= 1
            for j in range(i + 1, len(low_distance)):
                if i + 1 < len(low_distance):
                    for ind in distance_delete:
                        if list(low_distance.keys).__contains__(ind):
                            low_distance.pop()
        clust_centers, clust_index = list(cluster_centers.values()), []
        for i, clust in enumerate(clust_centers):
            if centers_delete.__contains__(clust):
                clust_index.append(clust_centers.index(clust))
                if len(clust_index) == 2:
                    clust_centers = clust_centers[:clust_index[0]] + [new_centers.pop(0)] + clust_centers[clust_index[0] + 1: clust_index[1]] + clust_centers[clust_index[1] + 1:]
        cluster_centers = {}
        for clust in clust_centers:
            cluster_centers.update({f"Z{len(cluster_centers) + 1}": clust})
        Nc = len(cluster_centers)
    return cluster_centers, Nc

def isodata(x_range, y_range):
    K = int(input("Кількість кластерів: "))
    iter_count = int(input("Максимальна кількість ітерацій: "))
    thetaN, thetaS, thetaC, L, Nc = krok1(1, 1, 3, 2, 1)
    clusters, points, iter = [], [], 1
    for y, x in enumerate(x_range):
        temp = [x, y_range[y]]
        points.append(temp)
    clust_centers, points_count = {}, len(points)
    if points:
        for j in range(0, Nc):
            clust_centers.update({f"Z{len(clust_centers) + 1}": points[j]})
    while iter <= iter_count:  # krok 14
        clusters, Ni, Nc = krok2(clust_centers, points)
        clusters, clust_centers, points, Ni, Nc, points_count = krok3(clusters, clust_centers, points, Ni, thetaN)
        clust_centers = krok4(clusters)
        cluster_distance = krok5(clusters, clust_centers, points)
        average_distance = krok6(cluster_distance, Ni, points_count)
        # krok 7
        if (iter == iter_count) or (iter % 2 == 0 or Nc >= K * 2):
            if iter == iter_count:
                thetaC = 0
            center_distance, center_indexes = krok11(clust_centers)
            low_center_distance = krok12(center_distance, center_indexes, thetaC, L)
            clust_centers, Nc = krok13(clust_centers, low_center_distance, Ni, Nc)
            iter += 1
        else:
            average_deviation = krok8(clusters, clust_centers, Ni)
            max_deviation, max_deviation_index = krok9(average_deviation)
            clust_centers, Nc, status = krok10(clust_centers, max_deviation, max_deviation_index, thetaS, Nc, K,
                                   cluster_distance, average_distance, thetaN, Ni)
            if not status:
                center_distance, center_indexes = krok11(clust_centers)
                low_center_distance = krok12(center_distance, center_indexes, thetaC, L)
                clust_centers, Nc = krok13(clust_centers, low_center_distance, Ni, Nc)
                iter += 1
            else:
                iter += 1
    return clusters, clust_centers

if __name__ == '__main__':
    x_axis, y_axis, points_name = points_input(False)
    plt.plot(x_axis, y_axis, 'o')
    plt.title("Вхідні дані")
    plt.xlabel("x")
    plt.ylabel("y")
    for j in range(len(x_axis)):
        cluster_point = [x_axis[j], y_axis[j]]
        plt.annotate(list(points_name.keys())[list(points_name.values()).index(cluster_point)], (x_axis[j], y_axis[j]))
    plt.grid()
    plt.show()
    cluster, clusters_center = isodata(x_axis, y_axis)
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
