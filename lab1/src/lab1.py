def square_splitting(N):
    if N % 2 == 0:
        half = N // 2
        return [
            (1, 1, half),
            (half + 1, 1, half),
            (1, half + 1, half),
            (half + 1, half + 1, half)
        ]
    elif N % 3 == 0:
        third = N // 3
        return [
            (1, 1, 2 * third),
            (2 * third + 1, 1, third),
            (1, 2 * third + 1, third),
            (2 * third + 1, third + 1, third),
            (third + 1, 2 * third + 1, third),
            (2 * third + 1, 2 * third + 1, third)
        ]
    
    grid = [[0] * N for _ in range(N)]
    best_placement = None

    def find_empty():
        for y in range(N):
            for x in range(N):
                if grid[y][x] == 0:
                    return x, y
        return None

    def can_place(x, y, s):
        if x + s > N or y + s > N:
            return False
        for dy in range(s):
            for dx in range(s):
                if grid[y + dy][x + dx] != 0:
                    return False
        return True

    def place(x, y, s, value):
        for dy in range(s):
            for dx in range(s):
                grid[y + dy][x + dx] = value

    def backtrack(count):

        nonlocal best_placement

        if best_placement is not None and count >= len(best_placement):
            return
        
        first_empty_position = find_empty()

        if first_empty_position is None:
            best_placement = current_placement.copy()
            return
        
        x, y = first_empty_position
        for s in range(min(N - x, N - y), 0, -1):
            if can_place(x, y, s):
                place(x, y, s, 1)
                current_placement.append((x + 1, y + 1, s))
                backtrack(count + 1)
                current_placement.pop()
                place(x, y, s, 0)

    current_placement = []
    a = (N + 1) // 2
    b = N - a
    fixed = [(a, a, a), (N - b + 1, 1, b), (1, N - b + 1, b)]
    for x, y, s in fixed:
        place(x - 1, y - 1, s, 1)

    backtrack(0)
    return fixed + best_placement



if __name__ == "__main__":
    N = int(input())
    result = square_splitting(N)
    print(len(result))
    for square in result:
        print(*square)
