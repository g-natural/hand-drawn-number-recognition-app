import tkinter as tk
import blockviewer as bv
import numpy as np
import os


class ViewChar(tk.Tk):
    ''' 
    View hand drawn characters from .csv files which specify 
    characters on a 28x28 canvas
    '''
    def __init__(self, input_matrix, graph=False, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.input_matrix = input_matrix
        self.graph = graph
        self.pic_count = len(input_matrix)-1
        self.canvas = bv.BlockViewer(self, 28, 28)
        self.canvas.grid(row=0, column=0)
        self.index_label = tk.Label(self)
        self.index_label.grid(row=1, column=0)

        if len(input_matrix) == 0:
            raise ValueError("Input matrix is empty")

        self.pic_index = 0
        self.canvas.view_picture(input_matrix[self.pic_index], self.graph)
        self.update_label()

        self.bind("<Left>", self.prev_picture)
        self.bind("<Right>", self.next_picture)

    def next_picture(self, event):
        if not (self.pic_index+1 > self.pic_count):
            self.pic_index += 1
            self.canvas.view_picture(self.input_matrix[self.pic_index], self.graph)
            self.update_label()

    def prev_picture(self, event):
        if not (self.pic_index <= 0):
            self.pic_index -= 1
            self.canvas.view_picture(self.input_matrix[self.pic_index], self.graph)
            self.update_label()

    def update_label(self):
        label_text = f"{self.pic_index}/{self.pic_count}"
        self.index_label.config(text=label_text)

def main():
    set_file_name = "training_60k_0.csv"
    set_file = open(os.path.join('assets', 'train_sets', set_file_name), 'rb')
    pics = np.loadtxt(set_file, delimiter=",", ndmin=2, max_rows=500)
    charviewer = ViewChar(pics, graph=True)
    charviewer.title(set_file_name)
    charviewer.mainloop()

if __name__ == '__main__':
    main()
