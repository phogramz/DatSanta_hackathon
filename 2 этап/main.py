import json
import sympy as sp
import numpy as np
import math
from pulp import *

from typing import List, Any
with open("gifts_value.json", 'r') as file2:
    information2 = json.load(file2)

with open("map(gifts).json", 'r') as file1:
    information = json.load(file1)

#Расчитываем матрицу ценности
ctr = 0
full_matrix_value = np.array([]) # матрица ценности 1000 детей х 5000 подарков
row = np.array([])
for item_ch in information['children']:
    row = np.array([])
    ctr += 1
    print(ctr)
    for item_gf in information['gifts']:
        for item_vl in information2['gifts_value']:
            if (item_vl['type'] == item_gf['type']) \
                    and (item_vl['gender'] == item_ch['gender']) \
                    and (item_vl['age'] == item_ch['age']):
                row = np.append(row, item_vl['value'] * math.log(item_gf['price'], 3))
    if item_ch == 0:
        full_matrix_value = np.array(row)
    else:
        full_matrix_value = np.concatenate(
            (full_matrix_value, row),
            axis=0
        )

# Решаем задачу о назначениях (транспортная задача)
problem = LpProblem('Открытая_транспортная_задача', LpMaximize)

# profit
matrix_unknown_values = np.array([])
for i in range(0, 1000):
    row = np.array([])
    for j in range(0, 5000):
        row = np.append(row, pulp.LpVariable(str(i) + " " + str(j), cat="Binary"))
    if i == 0:
        matrix_unknown_values = np.array(row)
    else:
        matrix_unknown_values = np.concatenate(
            (matrix_unknown_values, row),
            axis=0
        )

for i in matrix_unknown_values:
    problem += lpSum(i) == 1

problem += full_matrix_value.dot(matrix_unknown_values), "Function"
status = problem.solve()

print(status)
print("Общий СМР:", value(problem.objective))
