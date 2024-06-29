from dominate.tags import div, h5
from sudoku import Sudoku


def generate() -> div:
    generated_sudoku = Sudoku(3).difficulty(0.4).board
    print(generated_sudoku)
    for cell in generated_sudoku:
        print(cell)
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
                                            if curr_cell:
                                                h5(
                                                    curr_cell, cls="m-0",
                                                )
                                            else:
                                                h5(
                                                    0,
                                                    style="color:white;", cls="m-0",
                                                )  # Placeholder for Sudoku numbers is a white 0 to preserve cell height
    return sudoku_board
