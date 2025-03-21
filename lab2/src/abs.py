import numpy as np
 
from matrix import *


def tsp_abs(matrix, start):
    N = len(matrix)
    route = [start]
    path_cost = 0
    cur = start
    unvisited_vertexes = set(range(N)) - {start}

    while unvisited_vertexes: 
        
        next_vertex = min(unvisited_vertexes, key=lambda v: matrix[cur][v])

        path_cost += matrix[cur][next_vertex]
        route.append(next_vertex)
        unvisited_vertexes.remove(next_vertex)
        cur = next_vertex

    path_cost += matrix[cur][start]

    route.append(start)
    
    return route, path_cost



n = int(input("Введите количество городов (N): "))
sym = input("Симметричная матрица? (y/n): ").strip().lower() == 'y'

matrix = generate_matrix(n, symmetric=sym)

save_matrix(matrix, "data.txt")

loaded_matrix = load_matrix("data.txt")
print(loaded_matrix)

start = int(input("Введите индекс стартовой вершины (от 0 до N-1): "))
route, cost = tsp_abs(loaded_matrix, start)

print("Найденный маршрут: ", route)
print("Стоимость маршрута: ", cost)