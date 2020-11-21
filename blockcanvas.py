import tkinter as tk
import numpy as np

class BlockCanvas(tk.Canvas):
    # size in pixels of each block
    block_size = 15

    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        super().__init__(master, bg="grey",
                         width=self.width*self.block_size,
                         height=self.height*self.block_size)
        self.blockmatrix = np.full([width, height], 0.1, dtype=float)
        self.clear_canvas()

    # remove everything and fill canvas with white
    def clear_canvas(self):
        for item in self.find_all():
            self.delete(item)
        self.blockmatrix.fill(0)
        block_size = BlockCanvas.block_size
        self.create_rectangle(0, 0, self.width*block_size,
                              self.height*block_size, outline="white",
                              fill="white")

    def color_block(self, x, y):
        x = x // self.block_size
        y = y // self.block_size
        if(not (0 <= x < self.width) or not (0 <= y < self.height)):
            return
        if (self.blockmatrix[y][x] < 0.01):
            block_size = BlockCanvas.block_size
            self.blockmatrix[y][x] = .99
            xc = x * block_size
            yc = y * block_size
            self.create_rectangle(xc, yc, xc+block_size,
                                  yc+block_size, fill="black")
