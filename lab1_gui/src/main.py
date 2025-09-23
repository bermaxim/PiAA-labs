from gui import SquarePackingVisualizer

def main():
    N = int(input("Введите размер квадрата N (2-20): "))
    if 2 <= N <= 20:
        app = SquarePackingVisualizer(N)
        app.root.mainloop()
    else:
        print("N должно быть от 2 до 20")

if __name__ == "__main__":
    main()