######################################################
# FILE: boogle_gui.py
# WRITER: juman abu rmeleh, Adan Hammam
# EXERCISE: Intro2cs ex11 2022-2023
#####################################################
import tkinter as tk
from time import gmtime, strftime


class Cell:
    def __init__(self, parent, cell, text, callback):
        """ Create a cell button which will call the 'callback' function when being clicked with his location"""
        self.cell = cell
        self.box = tk.Button(parent, bg="pink", text=text, width=15, height=10, command=lambda: callback(self.cell),
                             bd=5, font=("Arial", 10))
        self.box.grid(row=cell[0], column=cell[1])


class Board:
    """ Create all the cells and store them"""

    def __init__(self, root, board, click_cell):
        self.frame = tk.Frame(root)
        self.cells = [[Cell(self.frame, (row, col), board[row][col], click_cell) for col in range(len(board[row]))] for
                      row in range(len(board))]

    def change_board(self, board):
        """ Update values and reset color of all cells in the board"""
        for row in range(len(board)):
            for col in range(len(board[row])):
                self.cells[row][col].box.configure(text=board[row][col], bg="pink")

    def update_buttons_state(self, state):
        """Update the state of the buttons: disabled or enabled"""
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                self.cells[row][col].box.configure(state=state)


class Timer:
    """This class, is used to create a timer object that can be used in a graphical user interface
        (GUI) application"""

    def __init__(self, root, callback, seconds):
        """Initializes the Timer object and sets the time for when the timer is reseted, creates a label that will
         display the timer and store the root, callback and the time."""
        # Store the time for when the timer is rested
        self.static_time = seconds
        self.time = seconds
        self.label = tk.Label(root, text=strftime("%M:%S", gmtime(self.time)), font=("Arial", 15))
        self.root = root
        # Function to call when the timer hits 0
        self.callback = callback

    def timer(self):
        """ This method updates the label to display the current time and checks if the time has reached 0. If it has,
         it calls the callback function. If not, it decrements the time by 1 and schedules the timer method to be
         called again in 1 second."""
        self.label.configure(text=strftime("Time: %M:%S", gmtime(self.time)))
        if self.time <= 0:
            self.callback()
        else:
            self.time -= 1
            self.root.after(1000, self.timer)

    def reset(self):
        """This method resets the time to the original value and updates the label to reflect the new time."""
        self.time = self.static_time
        self.label.configure(text=strftime("%M:%S", gmtime(self.time)))


class GUI:
    def __init__(self, board, click_cell, time_ended, seconds):
        self.root = tk.Tk()

        # creat the timer liable
        self.timer = Timer(self.root, time_ended, seconds)
        self.timer.label.grid(row=0, column=0)

        # creat the current word liable
        self.current_word = tk.Label(self.root, text="", font=("Arial", 15))
        self.current_word.grid(row=0, column=1)

        # creat the score liable
        self.score = tk.Label(self.root, text="Score: 0", font=("Arial", 15))
        self.score.grid(row=0, column=2)

        self.words = tk.Label(self.root, text="Words: ", font=("Arial", 10))
        self.words.grid(row=1, column=0, columnspan=2)

        # Create the new frame
        self.end_frame = tk.Frame(self.root)
        self.end_frame.grid(row=1, column=0, columnspan=3)
        self.end_frame.configure(bg="white")
        self.end_frame.grid_remove()

        # Create the "Play Again" button
        self.play_again_button = tk.Button(self.end_frame, text="Play Again", command=self.reset_game)
        self.play_again_button.grid(row=0, column=0)

        # Create the "Quit Game" button
        self.quit_button = tk.Button(self.end_frame, text="Quit Game", command=self.root.destroy)
        self.quit_button.grid(row=0, column=1)

        # creat the board
        self.board = Board(self.root, board, click_cell)
        self.board.frame.grid(row=2, column=0, columnspan=2)

    def reset(self, board):
        """This method resets the timer, score, current word and the words labels, and update the board."""
        self.timer.reset()
        self.score.configure(text="Score: 0")
        self.current_word.configure(text="")
        self.words.configure(text="Words: ")
        self.board.change_board(board)

    def reset_game(self):
        """This method is called when the "Play Again" button is clicked, it removes the end frame, resets the timer
         and enables the buttons again."""
        self.end_frame.grid_remove()
        self.board.update_buttons_state('normal')
        self.timer.reset()
        self.timer.timer()

    def time_ended(self):
        """This method is called when the timer reaches 0, it disables the buttons and shows the end frame."""
        self.board.update_buttons_state('disable')
        self.end_frame.grid()

    def run(self):
        """This method starts the main event loop of the Tkinter, making the window responsive to user inputs."""
        self.root.mainloop()
