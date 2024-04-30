import re
import os
import requests

# Example Sudoku board stored as a list of lists
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

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')  # Usually in the form "username/repo"
ISSUE_NUMBER = os.getenv('ISSUE_NUMBER')

def get_issue_title():
    # This function should extract the issue title from the GitHub event context
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['title']
    else:
        return None

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

def comment_and_close_issue(message):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}/comments'
    requests.post(url, headers=headers, json={"body": message})
    url_close = f'https://api.github.com/repos/{REPO_NAME}/issues/{ISSUE_NUMBER}'
    requests.patch(url_close, headers=headers, json={"state": "closed"})

def update_readme(number, row, column):
    # Simulated logic for updating README
    print("Updating README.md with the new move...")

def main():
    title = get_issue_title()
    if title is None:
        print("Failed to retrieve issue title.")
        return
    number, row, column = parse_move(title)
    if number is None or row is None or column is None:
        comment_and_close_issue("Failed to parse the move. Please check the format and try again.")
        return
    if is_valid_move(number, row, column):
        update_readme(number, row, column)
        print("README updated successfully.")
    else:
        comment_and_close_issue("Invalid move. Please try again with a valid Sudoku move.")

if __name__ == "__main__":
    main()
