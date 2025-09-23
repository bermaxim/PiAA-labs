class ReturnSearchProblemSolution:
    # --- инициализация ---
    def __init__(self, N):
        self.N = N
        self.grid = [[0] * N for _ in range(N)]
        self.current_placement = [] # кортеж (x1, y1, size)
        self.best_placement = None
        self.step_count = 0 
        self.is_auto = False # автоматизация для gui
        self.final_solution_shown = False

        self.special_case, self.fixed_squares = self.get_starting_squares()
        self.initialize_fixed_squares()

    # --- строим начальные квадраты --- 
    def get_starting_squares(self):
        if self.N % 2 == 0:  # N четное
            half = self.N // 2
            return "even", [(1, 1, half), 
                            (half + 1, 1, half), 
                            (1, half + 1, half), 
                            (half + 1, half + 1, half)]
        
        elif self.N % 3 == 0:  # N кратно 3
            third = self.N // 3
            return "three", [
                (1, 1, 2 * third), 
                (2 * third + 1, 1, third),
                (1, 2 * third + 1, third), 
                (2 * third + 1, third + 1, third),
                (third + 1, 2 * third + 1, third), 
                (2 * third + 1, 2 * third + 1, third)
            ]
        
        else:  # общий случай для остальных N
            a = (self.N + 1) // 2
            b = self.N - a
            return "backtrack", [(a, a, a), 
                                 (self.N - b + 1, 1, b), 
                                 (1, self.N - b + 1, b)]

    # --- описание начальной ситуации ---
    def get_case_description(self):
        if self.special_case == "even":
            return f"N={self.N} четное → решение состоит из 4 квадратов"
        elif self.special_case == "three":
            return f"N={self.N} кратно 3 → решение состоит из 6 квадратов"
        else:
            return f"Общий случай: старт из 3 фиксированных квадратов + backtracking"

    # --- работа с сеткой ---
    def set_square(self, x, y, size, value):
        for dy in range(size):
            for dx in range(size):
                self.grid[y + dy][x + dx] = value

    def can_place(self, x, y, size):
        if x + size > self.N or y + size > self.N:
            return False
        for dy in range(size):
            for dx in range(size):
                if self.grid[y + dy][x + dx] != 0:
                    return False
        return True

    def find_empty(self):
        for y in range(self.N):
            for x in range(self.N):
                if self.grid[y][x] == 0:
                    return x, y
        return None

    # --- алгоритм backtracking ---
    def backtrack_with_steps(self):
        if self.special_case in ["even", "three"]:
            yield f"✅ Оптимальное решение: {len(self.fixed_squares)} квадратов"
            return

        if self.best_placement and len(self.current_placement) >= len(self.best_placement):
            yield "❌ Отсечение: текущее решение хуже лучшего"
            return

        empty = self.find_empty()
        if not empty:
            if not self.best_placement or len(self.current_placement) < len(self.best_placement):
                self.best_placement = self.current_placement.copy()
                yield f"🎉 Новое оптимальное: {len(self.best_placement)} квадратов!"
            return

        x, y = empty
        max_size = min(self.N - x, self.N - y)
        for size in range(max_size, 0, -1):
            if self.best_placement and len(self.current_placement) + 1 >= len(self.best_placement):
                yield "❌ Отсечение по размеру"
                break
            if self.can_place(x, y, size):
                self.set_square(x, y, size, len(self.current_placement) + 1)
                self.current_placement.append((x + 1, y + 1, size))
                yield f"🟢 Размещён {size}×{size} в ({x + 1},{y + 1})"
                yield from self.backtrack_with_steps()
                self.set_square(x, y, size, 0)
                self.current_placement.pop()
        yield "↩️ Backtrack"

    # --- цвета ---
    def get_color(self, i):
        colors = ["#FF6B6B", "#49C6BD", "#45B7D1", "#96CEB4", "#FECA57", "#FF9FF3", "#54A0FF",
                  "#5F27CD", "#00D2D3", "#FF9F43", "#10AC84", "#EE5A24", "#A3CB38", "#ED4C67", "#B53471", "#6F1E51"]
        return colors[(i - 1) % len(colors)]

    # --- фиксируем начальные квадраты ---
    def initialize_fixed_squares(self):
        for i, (x, y, size) in enumerate(self.fixed_squares, 1):
            self.set_square(x - 1, y - 1, size, i)
            self.current_placement.append((x, y, size))
        if self.special_case in ["even", "three"]:
            self.best_placement = self.current_placement.copy()