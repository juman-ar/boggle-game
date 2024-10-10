####################################################
# FILE: ex11_utils.py
# WRITER: juman abu rmeleh, Adan Hammam
# EXERCISE: Intro2cs ex11 2022-2023
###################################################
from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]


def _is_valid_cell(cell, board):
    """checks if cell is in board"""
    return 0 <= cell[0] < len(board) and 0 <= cell[1] < len(board[0])


def _is_valid_neighbor(cell, neighbor):
    """checks if the cell that appears next to the current cell in one of the 8 directions (up, down, right, left
    or one of the four the diagonals). """
    return cell != neighbor and abs(cell[0] - neighbor[0]) <= 1 and abs(cell[1] - neighbor[1]) <= 1


def _path_to_word(path, board):
    """The function returns a string that is formed by concatenating the characters in the cells of the path, #
    in the order they appear in the path."""
    return "".join(board[cell[0]][cell[1]] for cell in path)


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """The function checks if the path is a valid path that describes a word that exists in the collection of words.
     If so, the function returns the found word."""
    last = None
    visited = set()
    word = ""
    for cell in path:  # If the path is invalid or the corresponding word does not exist in the dictionary,
        # the function will return None
        if not _is_valid_cell(cell, board) or (
                last is not None and not _is_valid_neighbor(cell, last)) or cell in visited:
            return None
        visited.add(cell)
        last = cell
        word += board[cell[0]][cell[1]]
    if word in words:
        return word
    return None


def _find_paths(n: int, board: Board, words: List, is_word_constant: bool) -> List:
    """This function is used to find all paths on a given board that form words from a given list of words"""
    paths = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            for path in _find_paths_helper((row, col), n, board, "", words, [[False for _ in range(len(board[0]))] for
                                                                             _ in range(len(board))], is_word_constant):
                if _path_to_word(path, board) in words:
                    paths.append(path)
    return paths


def _find_paths_helper(cell: Tuple, n: int, board: Board, word: str, words: list, visited, is_word_constant: bool) -> list:
    """This function is a helper function that is called recursively by the main function "_find_paths" to find all
    possible paths starting from a given cell on the board that form words from a given list of words."""
    new_word = word + board[cell[0]][cell[1]]

    possible_words = [w for w in words if w.startswith(new_word)]
    if not possible_words:  # if there's no words possible
        return []

    # Path length / Word Length
    if n == 1 or (is_word_constant and len(new_word) == len(possible_words[0])):
        return [[cell]]

    visited[cell[0]][cell[1]] = True
    paths = []
    for neighbor in [(cell[0] + y, cell[1] + x) for y in range(-1, 2) for x in range(-1, 2)]:
        #
        if _is_valid_cell(neighbor, board) and not visited[neighbor[0]][neighbor[1]]:
            paths.extend(
                _find_paths_helper(neighbor, n - 1, board, new_word, possible_words, visited, is_word_constant))

    visited[cell[0]][cell[1]] = False
    return [([cell] + path) for path in paths]


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """This function is used to find all paths on a given board that have a length of n and form words from a given
     list of words."""
    return _find_paths(n, board, [word for word in words if len(word) >= n], False)


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """The function returns a list of all valid paths describing words in the collection of words that are of
    length n"""
    return _find_paths(n, board, [word for word in words if len(word) == n], True)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """The function returns a list of valid paths that provide the maximum game score for the given board
    and word collection."""
    paths = {}
    for length in range(3, 16 + 1):
        paths.update((_path_to_word(path, board), path) for path in find_length_n_words(length, board, words))
    return list(paths.values())
