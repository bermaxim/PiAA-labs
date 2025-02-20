import time
import matplotlib.pyplot as plt
from lab1 import square_splitting


def measure_execution_time():
    sizes = list(range(2, 21))  
    times = []
    
    for N in sizes:
        start_time = time.time()
        square_splitting(N)
        end_time = time.time()
        times.append(end_time - start_time)
    
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, times, marker='o', linestyle='-', color='b', label='Время выполнения')
    plt.xlabel('Размер квадрата N')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Исследование времени выполнения алгоритма')
    plt.xticks(sizes) 
    plt.legend()
    plt.grid()
    plt.show()

measure_execution_time()
