# https://stackoverflow.com/questions/4954395/create-board-game-like-grid-in-python
import tkinter as tk
from PIL import Image, ImageTk

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=32, color1="white", color2="black"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

def count_attacking_queens(row_positions):
    '''
    https://discussions.udacity.com/t/ga-crossover-quiz/231503/2
    '''
    counter = 0
    for idx, num in enumerate(row_positions):
        for idx2, num2 in enumerate(row_positions):
            if idx != idx2:
                if num == num2:
                    counter += 1
                if int(num) == (int(num2) - abs(idx - idx2)):
                    counter += 1
                if int(num) == (int(num2) + abs(idx - idx2)):
                    counter += 1
    return str(counter/2)


if __name__ == "__main__":
    print(count_attacking_queens("32752124"))
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    # https://stackoverflow.com/questions/32649892/display-png-image-with-tkinter-and-pil
    # queen: https://commons.wikimedia.org/wiki/File:Chess_queen_icon.png
    image = Image.open('Chess_queen_icon.png')
    queen = ImageTk.PhotoImage(image)
    board.addpiece("queen1", queen, 8-3,0)
    board.addpiece("queen2", queen, 8-2,1)
    board.addpiece("queen3", queen, 8-7,2)
    board.addpiece("queen4", queen, 8-4,3)
    board.addpiece("queen5", queen, 8-2,4)
    board.addpiece("queen6", queen, 8-4,5)
    board.addpiece("queen7", queen, 8-1,6)
    board.addpiece("queen8", queen, 8-1,7)
    root.mainloop()
