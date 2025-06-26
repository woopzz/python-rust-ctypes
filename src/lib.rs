use std::slice;

const LINE_SIZE: usize = 16;
const BOX_SIZE: usize = 4;

#[unsafe(no_mangle)]
pub extern "C" fn solve_hexadoku(grid_ptr: *mut u8) -> bool {
    // We want to work with the grid as an array.
    let grid: &mut [u8] = unsafe { slice::from_raw_parts_mut(grid_ptr, LINE_SIZE * LINE_SIZE) };

    fn calc_flat_index(row_index: usize, col_index: usize) -> usize {
        row_index * LINE_SIZE + col_index
    }

    fn calc_box_index(row_index: usize, col_index: usize) -> usize {
        (row_index / BOX_SIZE) * BOX_SIZE + (col_index / BOX_SIZE)
    }

    let mut rows = [0u16; LINE_SIZE];
    let mut cols = [0u16; LINE_SIZE];
    let mut boxes = [0u16; LINE_SIZE];

    for i in 0..LINE_SIZE {
        for j in 0..LINE_SIZE {
            let flat_index = calc_flat_index(i, j);
            let val = grid[flat_index];
            if val != 0 {
                let bit = 1 << (val - 1);
                rows[i] |= bit;
                cols[j] |= bit;
                boxes[calc_box_index(i, j)] |= bit;
            }
        }
    }

    fn backtrack(
        grid: &mut [u8],
        pos: usize,
        rows: &mut [u16; LINE_SIZE],
        cols: &mut [u16; LINE_SIZE],
        boxes: &mut [u16; LINE_SIZE],
    ) -> bool {
        if pos == LINE_SIZE * LINE_SIZE {
            return true;
        }

        let flat_index = pos;
        if grid[flat_index] != 0 {
            return backtrack(grid, pos + 1, rows, cols, boxes);
        }

        let row_index = pos / LINE_SIZE;
        let col_index = pos % LINE_SIZE;
        let box_index = calc_box_index(row_index, col_index);

        for num in 1..=LINE_SIZE as u8 {
            let bit = 1 << (num - 1);
            if (rows[row_index] & bit) != 0
                || (cols[col_index] & bit) != 0
                || (boxes[box_index] & bit) != 0 {
                continue;
            }

            grid[flat_index] = num;
            rows[row_index] |= bit;
            cols[col_index] |= bit;
            boxes[box_index] |= bit;

            if backtrack(grid, pos + 1, rows, cols, boxes) {
                return true;
            }

            grid[flat_index] = 0;
            rows[row_index] &= !bit;
            cols[col_index] &= !bit;
            boxes[box_index] &= !bit;
        }
        false
    }

    backtrack(grid, 0, &mut rows, &mut cols, &mut boxes)
}
