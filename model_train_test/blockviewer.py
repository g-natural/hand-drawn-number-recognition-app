from tkinter import *
import numpy as np
import sys

class BlockViewer(Canvas):
    # size in pixels of each block
    block_size = 15

    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        super().__init__(master, bg="grey",
                         width=self.width*self.block_size,
                         height=self.height*self.block_size)
        self.blockmatrix = np.full([width, height], 0, dtype=float)
        self.clear_canvas()

    # remove everything and fill canvas with white
    def clear_canvas(self):
        for item in self.find_all():
            self.delete(item)
        self.blockmatrix.fill(False)
        block_size = BlockViewer.block_size
        self.create_rectangle(0, 0, self.width*block_size,
                              self.height*block_size, outline="white",
                              fill="white")

    def view_picture(self, vector, graph=False):
        self.clear_canvas()
        if vector.size != (self.width * self.height):
            sys.stderr.write("vector size invalid")
            return

        for y in range(self.width):
            for x in range(self.height):
                vector_loc = (y*self.width)+x
                color = hex(int(255-(vector[vector_loc] * 255)))
                if len(color) == 3:
                    color = "0" + color[-1]
                else:
                    color = color[-2:]
                color = "#" + color + color + color
                if(graph):
                    o_color = "black"
                else:
                    o_color = color
                block_size = BlockViewer.block_size
                xc = x * block_size
                yc = y * block_size
                self.create_rectangle(xc, yc, self.width*block_size,
                                      self.height*block_size,
                                      outline=o_color, fill=color)
