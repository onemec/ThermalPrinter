from dominate.tags import div, h5
import sudoku


def generate() -> div:
    generated_sudoku = sudoku.generate()
    sudoku_board = div(cls="container")
    with sudoku_board:
        for out_row in range(3):
            with div(cls="row g-0"):
                for out_col in range(3):
                    with div(cls="col border border-black"):
                        with div(cls="container p-0"):
                            for in_row in range(3):
                                with div(cls="row g-0"):
                                    for in_col in range(3):
                                        with div(cls="col border p-2 text-center"):
                                            curr_cell = generated_sudoku[
                                                out_row * 3 + in_row
                                            ][out_col * 3 + in_col]
                                            h5(
                                                curr_cell if curr_cell != 0 else " ",
                                                cls="m-0",
                                            )  # Placeholder for Sudoku numbers
    return sudoku_board
