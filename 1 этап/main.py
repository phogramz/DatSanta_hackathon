import json
import sympy as sp
from multiprocessing import Pool


def len_line(item1, item2, circls):
    point1_base = sp.Point2D(item1['x'], item1['y'])
    point2_base = sp.Point2D(item2['x'], item2['y'])
    result_len = point1_base.distance(point2_base)
    incircls_len = 0

    Line = sp.Segment(point1_base, point2_base)
    for item_circl in circls:
        PointCircle = sp.Point2D(item_circl['x'], item_circl['y'])
        if item_circl['r'] < Line.distance(PointCircle):
            #print("далеко")
            continue
        Circl = sp.Circle(PointCircle, item_circl['r'])
        two_points = Circl.intersection(Line)
        if len(two_points) >= 2:
            incircls_len += two_points[0].distance(two_points[1])

    result_len += incircls_len * 6
    return result_len


if __name__ == "__main__":
    with open("map.json", 'r') as file:
        information = json.load(file)

    matrix_len = []
    i = 0
    pool = Pool(processes=8)
    for item in information['children']: # считаем матрицу расстояния
        row = []
        i += 1
       # print(i)
        j = 0
        for itm in information['children']:
            #row.append(float(pool.apply_async(len_line, (item, itm, information['snowAreas'])).get()))
            row.append(pool.apply_async(len_line, (item, itm, information['snowAreas'])))
            j += 1
            #print(j)
        matrix_len.append(row)
    for j in matrix_len:
        for i in j:
            print(int(i.get()), end=' ')
        print(" ")