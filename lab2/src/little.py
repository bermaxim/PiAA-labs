import numpy as np
from matrix import  *

INF = np.inf
best_cost = INF
best_path = []

def reduce_matrix(matrix):
    delta = 0
    reduced_matrix = np.copy(matrix) 
    size = reduced_matrix.shape[0]
    
    for i in range(size):
        row_min = np.min(reduced_matrix[i])
        if row_min == INF:
            continue 
        delta += row_min
        reduced_matrix[i] -= row_min

    for j in range(size):
        col_min = np.min(reduced_matrix[:, j])
        if col_min == INF:
            continue  
        delta += col_min
        reduced_matrix[:, j] -= col_min 

    return reduced_matrix, delta


def get_greatest_zero(matrix, current_node):
    size = matrix.shape[0]
    degrees = []
    
    for j in range(size):
        if matrix[current_node][j] == 0:
            row_min = np.min(matrix[current_node][np.arange(size) != j])
            row_min = row_min if row_min != INF else 0
            
            col_min = np.min(matrix[np.arange(size) != current_node, j])
            col_min = col_min if col_min != INF else 0
            
            degrees.append((current_node, j, row_min + col_min))
    
    return sorted(degrees, key=lambda x: -x[2])

def prim_mst(submatrix):
    size = submatrix.shape[0]
    if size <= 1:
        return 0
    
    selected = {0}
    mst_cost = 0

    while len(selected) < size:
        min_edge = INF
        best_vertex = None

        for u in selected:
            for v in range(size):
                if v not in selected and matrix[u, v] < min_edge:
                    min_edge = matrix[u, v]
                    best_vertex = v
        selected.add(best_vertex)
        mst_cost += min_edge
    
    return mst_cost

def calculate_bound(pieces, matrix):
    if not pieces:
        return 0
    
    size = len(pieces)
    submatrix = np.full((size, size), INF)
    
    for i in range(size):
        for j in range(i + 1, size):
            start_i, end_i = pieces[i]
            start_j, end_j = pieces[j]
            w = min(matrix[end_i][start_j], matrix[end_j][start_i])
            submatrix[i][j] = submatrix[j][i] = w
    
    return prim_mst(submatrix)

def branching(matrix, path, cost, pieces, start):
    global best_cost, best_path
    n = matrix.shape[0]
    
    if len(path) == n:
        final_cost = cost + matrix[path[-1]][start]
        if final_cost < best_cost:
            best_cost = final_cost
            best_path = path + [start]
        return
    
    bound = calculate_bound(pieces, matrix)
    if cost + bound >= best_cost:
        return
    
    current_node = path[-1]
    zero_degrees = get_greatest_zero(matrix, current_node)
    
    if not zero_degrees:
        return
    
    for current, next_node, _ in zero_degrees:
        if next_node in path or matrix[current][next_node] == INF:
            continue
            
        new_pieces = pieces.copy()
        merged = False
        for i, (s, e) in enumerate(new_pieces):
            if e == current:
                new_pieces[i] = (s, next_node)
                merged = True
            elif s == next_node:
                new_pieces[i] = (current, e)
                merged = True
        if not merged:
            new_pieces.append((current, next_node))
        
        new_mat = np.copy(matrix)
        new_mat[current, :] = INF
        new_mat[:, next_node] = INF
        new_mat[next_node, current] = INF
        
        reduced_mat, reduction_cost = reduce_matrix(new_mat)
        new_cost = cost + matrix[current][next_node] + reduction_cost
        branching(reduced_mat, path + [next_node], new_cost, new_pieces, start)
        
        new_mat_right = np.copy(matrix)
        new_mat_right[current][next_node] = INF
        reduced_right, reduction_right = reduce_matrix(new_mat_right)
        branching(reduced_right, path, cost + reduction_right, pieces, start)
        break


def solve_little(matrix):
    global best_cost, best_path
    all_best_cost = INF
    all_best_path = []
    n = matrix.shape[0]
    
    for start in range(n):
        best_cost = INF  
        best_path = []
        
        reduced_mat, init_cost = reduce_matrix(matrix)
        branching(reduced_mat, [start], init_cost, [], start)
        
        if best_cost < all_best_cost:
            all_best_cost = best_cost
            all_best_path = best_path
    
    return all_best_path, all_best_cost


# if __name__ == "__main__":
#     n = int(input())
#     matrix = []
#     for _ in range(n):
#         row = list(map(int, input().split()))
#         matrix.append([float('inf') if x == -1 else float(x) for x in row])

    
#     matrix = np.array(matrix, dtype=np.float64)
#     path, cost = solve_little(matrix)
#     print(" ".join(map(str, path[:-1])))
#     print(cost)



n = int(input("Введите количество городов (N): "))
sym = input("Симметричная матрица? (y/n): ").strip().lower() == 'y'

matrix = generate_matrix(n, symmetric=sym)

save_matrix(matrix, "data.txt")

loaded_matrix = load_matrix("data.txt")
print(loaded_matrix)

route, cost = solve_little(loaded_matrix)

print("Найденный маршрут: ", route)
print("Стоимость маршрута: ", cost)
