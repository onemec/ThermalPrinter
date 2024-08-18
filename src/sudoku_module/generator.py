from dominate.tags import div, h5
from sudoku import Sudoku


def generate() -> div:
    """
    Generates a Sudoku board with a specified difficulty and returns it as a DOM structure.

    The function creates a 9x9 Sudoku board divided into 3x3 subgrids. Each cell in the board
    is styled to have equal width and height, and empty cells are displayed with white text.

    Returns:
        div: A DOM structure representing the Sudoku board.
    """
    generated_sudoku = (
        Sudoku(3).difficulty(0.4).board
    )  # Generate a 9x9 Sudoku board with 40% difficulty
    sudoku_board = div(
        cls="container"
    )  # Create the main container for the Sudoku board

    for out_row in range(3):
        with sudoku_board.add(div(cls="row g-0")):  # Create a row for each 3x3 subgrid
            for out_col in range(3):
                with div(
                    cls="col border border-black"
                ):  # Create a column for each 3x3 subgrid
                    with div(
                        cls="container p-0"
                    ):  # Create a container for the cells within the subgrid
                        for in_row in range(3):
                            with div(
                                cls="row g-0"
                            ):  # Create a row for each cell within the subgrid
                                for in_col in range(3):
                                    curr_cell = generated_sudoku[out_row * 3 + in_row][
                                        out_col * 3 + in_col
                                    ]  # Get the current cell value
                                    cell_value = (
                                        curr_cell if curr_cell else 0
                                    )  # Use 0 for empty cells
                                    cell_style = (
                                        {} if curr_cell else {"style": "color:white;"}
                                    )  # Style empty cells with white text
                                    div(cls="col border p-2 text-center").add(
                                        h5(cell_value, cls="m-0", **cell_style)
                                    )  # Create the cell with the appropriate value and style

    return sudoku_board  # Return the generated Sudoku board
