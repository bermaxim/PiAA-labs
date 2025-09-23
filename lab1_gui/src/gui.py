import tkinter as tk
from solver import ReturnSearchProblemSolution

class SquarePackingVisualizer:
    def __init__(self, N):
        self.N = N
        self.root = tk.Tk()
        self.root.title(f"Разбиение квадрата {N}x{N} - Backtracking")
        self.root.geometry("1200x750")

        # --- разметка контейнеров (frames) ---
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self.main_frame, width=300)
        self.right_frame.pack(side="right", fill="y", padx=10)
        self.right_frame.pack_propagate(False)

        # --- левая панель (Canvas) ---
        self.cell_size = 500 // N
        self.canvas_size = self.cell_size * N + 50
        self.canvas = tk.Canvas(self.left_frame, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(pady=10)

        # --- правая панель (результаты) ---
        self.results_text = tk.Text(self.right_frame, width=35, height=20, font=("Courier New", 10))
        self.results_text.pack(fill="both", expand=True)
        self.results_text.config(state="disabled")

        # --- панель управления (кнопки действий)---
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=5)

        self.step_button = tk.Button(self.control_frame, text="Следующий шаг", command=self.next_step)
        self.step_button.pack(side="left", padx=5)

        self.auto_button = tk.Button(self.control_frame, text="Авто", command=self.toggle_auto)
        self.auto_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Сброс", command=self.reset)
        self.reset_button.pack(side="left", padx=5)

        # --- информационные метки ---
        self.info_label = tk.Label(self.root, text="", font=("Arial", 12), wraplength=800)
        self.info_label.pack(pady=5)

        # --- информация о краткой статистике ---
        self.stats_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.stats_label.pack()

        # --- solver ---
        self.solver = ReturnSearchProblemSolution(N)
        self.step_generator = self.solver.backtrack_with_steps()

        # -- рисуем сетку и выводим описание случая ---
        self.draw_grid()
        self.update_info(self.solver.get_case_description())

    # --- UI методы ---
    def draw_grid(self, final=False):
        self.canvas.delete("all")
        # сетка
        for i in range(self.N + 1):
            self.canvas.create_line(25 + i * self.cell_size, 25,
                                    25 + i * self.cell_size, 25 + self.N * self.cell_size, fill="lightgray")
            self.canvas.create_line(25, 25 + i * self.cell_size,
                                    25 + self.N * self.cell_size, 25 + i * self.cell_size, fill="lightgray")

        # квадраты
        squares = self.solver.best_placement if final and self.solver.best_placement else self.solver.current_placement
        for i, (x, y, size) in enumerate(squares, 1):
            color = self.solver.get_color(i)
            x1, y1 = 25 + (x - 1) * self.cell_size, 25 + (y - 1) * self.cell_size
            x2, y2 = x1 + size * self.cell_size, y1 + size * self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=4 if final else 2, fill=color)
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(size), font=("Arial", 12, "bold"))

        # подсветка
        if not final:
            empty = self.solver.find_empty()
            if empty:
                x, y = empty
                x1, y1 = 25 + x * self.cell_size, 25 + y * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

    def update_info(self, msg):
        self.info_label.config(text=msg)
        stats = f"Шагов: {self.solver.step_count} | Текущих квадратов на сетке: {len(self.solver.current_placement)}"
        if self.solver.best_placement:
            stats += f" | Лучшее решение: {len(self.solver.best_placement)}"
        self.stats_label.config(text=stats)

    def show_final_solution(self):
        self.draw_grid(final=True)
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, "end")
        txt = f"🔥 ОПТИМАЛЬНОЕ РЕШЕНИЕ\nN = {self.N} | Квадратов: {len(self.solver.best_placement)}\n"
        txt += "=" * 30 + "\n"
        for i, (x, y, size) in enumerate(self.solver.best_placement, 1):
            txt += f"{i:2d}) x = {x}, y = {y}, size = {size}\n"
        self.results_text.insert(1.0, txt)
        self.results_text.config(state="disabled")

    # --- управление шагами ---
    def next_step(self):
        try:
            msg = next(self.step_generator)
            self.solver.step_count += 1
            self.update_info(msg)
            self.draw_grid()
        except StopIteration:
            self.update_info("🎬 Алгоритм завершён")
            if self.solver.best_placement:
                self.show_final_solution()
            self.step_button.config(state="disabled")
            self.auto_button.config(state="disabled")

    # --- автоматизация ---
    def toggle_auto(self):
        self.solver.is_auto = not self.solver.is_auto
        self.auto_button.config(
            text="Стоп" if self.solver.is_auto else "Авто",
            bg="red" if self.solver.is_auto else "SystemButtonFace"
        )
        self.step_button.config(state="disabled" if self.solver.is_auto else "normal")
        if self.solver.is_auto:
            self.auto_play()

    def auto_play(self):
        if self.solver.is_auto:
            self.next_step()
            self.root.after(100 if self.N > 6 else 200, self.auto_play)

    def reset(self):
        self.__init__(self.N)