import time

LINE_SIZE = 16
BOX_SIZE = 4

def log_time_taken(tag):
    def wrap(func):
        def wrap_wrap(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            print(f'[{tag}] Time taken: {end_time - start_time:.4f} seconds')
            return result
        return wrap_wrap
    return wrap

@log_time_taken('python')
def run_py(grid):
    def calc_flat_index(row_index, col_index):
        return row_index * LINE_SIZE + col_index

    def calc_box_index(row_index, col_index):
        return (row_index // BOX_SIZE) * BOX_SIZE + (col_index // BOX_SIZE)

    rows = [set() for _ in range(LINE_SIZE)]
    cols = [set() for _ in range(LINE_SIZE)]
    boxes = [set() for _ in range(LINE_SIZE)]

    for i in range(LINE_SIZE):
        for j in range(LINE_SIZE):
            flat_index = calc_flat_index(i, j)
            val = grid[flat_index]
            if val:
                rows[i].add(val)
                cols[j].add(val)
                boxes[calc_box_index(i, j)].add(val)

    def backtrack(pos):
        if pos == LINE_SIZE * LINE_SIZE:
            return True

        flat_index = pos
        if grid[flat_index]:
            return backtrack(pos + 1)

        row_index, col_index = divmod(pos, LINE_SIZE)
        box_index = calc_box_index(row_index, col_index)

        for num in range(1, LINE_SIZE + 1):
            if (
                num in rows[row_index]
                or num in cols[col_index]
                or num in boxes[box_index]
            ):
                continue

            grid[flat_index] = num
            rows[row_index].add(num)
            cols[col_index].add(num)
            boxes[box_index].add(num)

            if backtrack(pos + 1):
                return True

            grid[flat_index] = 0
            rows[row_index].remove(num)
            cols[col_index].remove(num)
            boxes[box_index].remove(num)

        return False

    return backtrack(0)

@log_time_taken('rust')
def run_rust(grid):
    import ctypes

    lib = ctypes.CDLL('./target/release/libdemo.so')

    lib.solve_hexadoku.argtypes = [ctypes.POINTER(ctypes.c_uint8)]
    lib.solve_hexadoku.restype = ctypes.c_bool

    arr = (ctypes.c_ubyte * (LINE_SIZE * LINE_SIZE))(*grid)
    return lib.solve_hexadoku(arr)

if __name__ == '__main__':
    example_grid = [
        0, 0,  0,  0,     0, 10, 0, 0,     4,  0,  0, 0, 0,    12, 0, 0,
        0, 0,  0, 12,    13,  0, 0, 0,     0,  0, 15, 0, 0,     0, 0, 0,
        0, 0,  0,  0,     0,  0, 0, 3,    14,  0,  0, 0, 5,     0, 0, 0,
        0, 0, 13,  0,     0,  0, 0, 0,     0, 10,  0, 0, 0,     0, 0, 0,
    ]
    example_grid += [0] * (LINE_SIZE * LINE_SIZE - len(example_grid))
    print('[python] Result:', run_py(example_grid))
    print('[rust] Result:', run_rust(example_grid))
