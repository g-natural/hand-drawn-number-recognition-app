import tkinter as tk
import CRNNetwork as cr
import blockcanvas as bc
import correction_popup as cp
import numpy as np
import pickle
import os
import pdb


class NumRecApp(tk.Tk):

    def __init__(self, network, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.title("Number Recognition")
        self.geometry("725x500")
        self.resizable(False, False)

        if isinstance(network, cr.CRNNetwork):
            self.network = network
        else:
            return None

        # 'Drawing' section of window (left side)
        drawing_frame = tk.Frame(self, padx=20, pady=20)
        drawing_top_label = tk.Label(drawing_frame, text="Draw a number (0-9)")
        self.drawing_canvas = bc.BlockCanvas(drawing_frame, width=28, height=28)
        clear_button = tk.Button(drawing_frame, text="clear", padx=25, pady=7)
        clear_button.config(command=self.clear)

        drawing_frame.grid(row=0, column=0)
        drawing_top_label.grid(row=0, column=0)
        self.drawing_canvas.grid(row=1, column=0)
        clear_button.grid(row=2, column=0)

        # 'Interpreting' section of the window (right side)
        interpret_frame = tk.Frame(self, padx=10, pady=10)
        interpret_top_label = tk.Label(interpret_frame)
        interpret_top_label.config(text="Character interpreted as:")
        # additional frame to make white number background larger
        num_background = tk.Frame(
            interpret_frame, bg="white", padx=75, pady=35)
        self.num_display_label = tk.Label(num_background, text="0")
        self.num_display_label.configure(bg="white", fg="white")
        self.num_display_label.configure(font=("Serif", 100))
        interpret_button = tk.Button(
            interpret_frame, text="Interpret", padx=25, pady=10)
        interpret_button.config(command=self.interpret)
        incorrect_button = tk.Button(
            interpret_frame, text="Incorrect", padx=25, pady=10)
        incorrect_button.config(command=self.correction)

        interpret_frame.grid(row=0, column=1)
        interpret_top_label.grid(row=0, column=0)
        num_background.grid(row=1, column=0)
        self.num_display_label.grid(row=0, column=0)
        interpret_button.grid(row=2, column=0)
        incorrect_button.grid(row=4, column=0, sticky="s")

        # popup window for corrections to network
        self.corr_popup = cp.CorrectionPopup(self)
        self.corr_popup.withdraw()  # hide until needed

        self.drawing_canvas.bind('<B1-Motion>', self.draw)
        self.drawing_canvas.bind('<ButtonPress-1>', self.draw)
        self.bind("<<CorrectionRequest>>", self.update_network)
        self.bind("<<CorrectionCancel>>", self.correction_return)

    def interpret(self):
        vector = self.drawing_canvas.blockmatrix.ravel()
        vector = np.array([vector])
        pdb.set_trace()
        answer = self.network.query_network(vector[0])
        self.set_number(answer.argmax())
        return answer

    def set_number(self, num):
        if(num >= 0 and num <= 9):
            self.num_display_label.configure(fg="black")
            self.num_display_label['text'] = num
        else:
            raise ValueError('Number not between 0-9')

    def draw(self, event):
        self.drawing_canvas.color_block(event.x, event.y)

    def clear(self):
        self.drawing_canvas.clear_canvas()
        self.num_display_label.configure(fg="white")

    def correction(self):
        self.grab_set()
        # center on current window
        new_x = int(self.winfo_x() + (self.winfo_width()/4))
        new_y = int(self.winfo_y() + (self.winfo_height()/4))

        self.corr_popup.geometry(f"+{new_x}+{new_y}")
        self.corr_popup.deiconify()

    def correction_return(self, event):
        self.grab_release()
        self.corr_popup.withdraw()

    def update_network(self, event):
        self.grab_release()
        self.corr_popup.withdraw()


def main():
    model_file = os.path.join("model", "NumRecNet_rand600k_epoch36_nodes28_.pkl")
    network = pickle.load(open(model_file, 'rb'))
    app = NumRecApp(network)
    app.mainloop()


if __name__ == '__main__':
    main()
