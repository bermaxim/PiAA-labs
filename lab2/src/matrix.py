import numpy as np

def generate_matrix(n, symmetric=False):
    if symmetric:
        A = np.random.randint(1, 100, size=(n, n)).astype(float)
        A = (A + A.T) // 2 
    else:
        A = np.random.randint(1, 100, size=(n, n)).astype(float)
    np.fill_diagonal(A, np.inf)  
    return A


def save_matrix(matrix, filename="data.txt"):
    np.savetxt(filename, matrix, delimiter=',', fmt='%g')

def load_matrix(filename="data.txt"):
    return np.loadtxt(filename, delimiter=',')