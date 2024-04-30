import re
import os

# Example Sudoku board stored as a list of lists
# This should ideally be dynamically read from README.md
sudoku_board = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9]
]

def get_issue_title():
    # This function should extract the issue title from the GitHub event context
    # For the sake of example, let's assume the title is "Move 5 at B3"
    return "Move 5 at B3"

def parse_move(title):
    # Extract the move and position from the title
    match = re.match(r"Move (\d) at ([A-I])(\d)", title)
    if not match:
        return None, None, None
    number = int(match.group(1))
    column = ord(match.group(2)) - ord('A')
    row = int(match.group(3)) - 1
    return number, row, column

def is_valid_move(number, row, column):
    # Validate the move on the Sudoku board
    # Check row, column, and the 3x3 grid
    row_vals = sudoku_board[row]
    if number in row_vals:
        return False
    col_vals = [sudoku_board[i][column] for i in range(9)]
    if number in col_vals:
        return False
    # Check the 3x3 square
    start_row, start_col = 3 * (row // 3), 3 * (column // 3)
    for i in range(3):
        for j in range(3):
            if sudoku_board[start_row + i][start_col + j] == number:
                return False
    return True

def update_readme(number, row, column):
    # Load README.md
    with open("README.md", "r") as file:
        lines = file.readlines()

    # Logic to update the specific line and column in the README
    # This is simplified and may need adjustment based on your actual README layout
    line_index = 2 + row  # Assuming the board starts at line 2
    line = lines[line_index]
    new_line = line[:6 + 4 * column] + str(number) + line[7 + 4 * column:]
    lines[line_index] = new_line

    # Write the updated README.md back
    with open("README.md", "w") as file:
        file.writelines(lines)

def main():
    title = get_issue_title()
    number, row, column = parse_move(title)
    if number is None or row is None or column is None:
        print("Failed to parse move.")
        return
    if is_valid_move(number, row, column):
        update_readme(number, row, column)
        print("README updated successfully.")
    else:
        print("Invalid move. No update performed.")

if __name__ == "__main__":
    main()
