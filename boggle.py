############################################################
# FILE: boogle.py
# WRITER: juman abu rmeleh, Adan Hammam
# EXCERSISE: Intro2cs ex11 2022-2023
# DESCRIPTION: This is a script for a game called "Boggle". Boggle is a word game where players try to find as many
# words as possible on a 4x4 grid of letters. The script uses the tkinter library to create a graphical user
# interface (GUI) for the game
############################################################

from boggle_board_randomizer import randomize_board
from ex11_utils import _is_valid_neighbor, _path_to_word
from boggle_gui import GUI

GAME_LENGTH = 60 * 3
DEFAULT_BOARD = [["Click", "On", "Any", "Cell"], ["To", "Start", "The", "Game"], ["", "", "", ""], ["", "", "", ""]]
END_GAME_DELAY = 2 * 1000


class Game:
    def reset_game(self):
        """This method sets up a new game by generating a new random board, clearing the current path and words,
         and resetting the score to 0"""
        self.board = randomize_board()
        self.path = []
        self.score = 0
        self.words = []
        self.started = False
        self.gui.reset(self.board)

    def reset_game1(self):
        """This method is called when the "Play Again" button is clicked, it hides the end frame and start a new game"""
        self.gui.end_frame.grid_remove()  # hide the new frame
        self.start_game()

    def quit_game(self):
        """This method is called when the "Quit Game" button is clicked, it closes the game's window."""
        self.gui.root.destroy()

    def __init__(self):
        """Initializes the Game object and creates an instance of the GUI class and loads the words from the
        boggle_dict.txt file, it also sets the started flag to False"""
        self.gui = GUI(DEFAULT_BOARD, self.click_cell, self.end_game, int(GAME_LENGTH))
        self.started = False
        with open('boggle_dict.txt', 'r') as f:
            self.dictionary = f.read().split("\n")[:-1]

    def click_cell(self, cell):
        """This method is called when a cell on the board is clicked. It updates the current path, current word and
         checks if the current path is a word in the dictionary and updates the score and words list accordingly."""
        # start the game if it hasn't been started yet
        if not self.started:
            self.start_game()
            return

        # if the cell is already in the current path, remove it from the path
        if cell in self.path:
            if self.path[-1] == cell:
                self.path.remove(cell)
                self.gui.board.cells[cell[0]][cell[1]].box.configure(bg="pink")
                self.refresh_word()
            return

        # return if the clicked cell is not a valid neighbor of the last cell in the path
        if len(self.path) > 0 and not _is_valid_neighbor(self.path[-1], cell):
            return

        # add the cell to the current path and update the GUI
        self.path.append(cell)
        self.gui.board.cells[cell[0]][cell[1]].box.configure(bg="aquamarine")
        self.refresh_word()

        # check if the current path forms a valid word in the dictionary
        current_word = _path_to_word(self.path, self.board)

        # if it is a valid word, update the score and words list and update the GUI
        if current_word in self.dictionary and current_word not in self.words:
            self.words.append(current_word)
            self.gui.words.configure(text=f"Words: {', '.join(self.words)}")

            self.score += len(self.path) ** 2
            self.gui.score.configure(text=f"Score: {self.score}")

            # change the color of the cells in the current path to pink
            for cell in self.path:
                self.gui.board.cells[cell[0]][cell[1]].box.configure(bg="pink")

            self.path = []
            self.refresh_word()

    def refresh_word(self):
        """ This method updates the current word label to match the current path"""
        self.gui.current_word.configure(text=_path_to_word(self.path, self.board))

    def start_game(self):
        """This method starts the game by resetting the game and starting the timer"""
        self.reset_game()
        self.started = True
        self.gui.timer.timer()

    # End game and add a delay of 'END_GAME_DELAY' seconds so the player won't start playing again when try into type
    # words
    def end_game(self):
        """This method ends the game by disabling the buttons on the board, showing the end frame with the play again
        and quit button and resetting the game and board."""
        self.gui.board.update_buttons_state("disabled")
        self.gui.end_frame.grid()  # show the new frame with the buttons
        self.started = False
        self.gui.board.change_board(DEFAULT_BOARD)

    def run(self):
        """This method starts the main event loop of the Tkinter, making the window responsive to user inputs"""
        self.gui.run()


Game().run()
