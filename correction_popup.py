import tkinter as tk


class numButton(tk.Button):
    def __init__(self, parent, num):
        super().__init__(parent, text=num, padx=25, pady=10,
                         command=self.pressed)
        self.parent = parent
        self.num = num

    def pressed(self):
        self.parent.event_generate("<<NumButtonPressed>>", x=self.num)


class CorrectionPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Correction")
        self.resizable(False, False)

        self.parent = parent
        # create numpad
        buttons = []
        # calculate row to make layout like a calculator
        calc_row = lambda num: (3 if(num<=3) else 2 if(num<=6)
                                else 1 if(num<=9) else -1)
        for i in range(1, 10):
            button = numButton(self, i)
            button.grid(row=calc_row(i), column=((i-1) % 3))
            buttons.append(button)
        # add in zero
        buttons.append(numButton(self, 0).grid(row=4, column=0))

        top_label = tk.Label(self, text="Enter the correct number:")
        top_label.config(font=("Times New Roman", 12))
        self.num_label = tk.Label(self, bg="white", text="9", fg="white", padx=45)
        self.num_label.configure(font=("Serif", 100))

        apply_button = tk.Button(self, text="Apply", padx=20, pady=8)
        apply_button.config(command=self.apply_correction)
        cancel_button = tk.Button(self, text="Cancel", padx=20, pady=8)
        cancel_button.config(command=self.cancel)
        warning = "Warning: supplying wrong information will train the model to be less accurate"
        warning_label = tk.Label(self, text=warning, font=("Serif", 8))

        top_label.grid(row=0, column=0, columnspan=3)
        self.num_label.grid(row=1, column=3, rowspan=3)
        apply_button.grid(row=4, column=3, sticky="ne")
        cancel_button.grid(row=4, column=3, sticky="nw")
        warning_label.grid(row=5, column=0, columnspan=4)

        self.bind("<<NumButtonPressed>>", self.set_num)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def set_num(self, event):
        self.num_label.configure(fg="black")
        self.num_label['text'] = event.x
        self.selected_num = event.x

    def apply_correction(self):
        self.parent.event_generate("<<CorrectionRequest>>", x=self.selected_num)
        self.num_label.configure(fg="white")

    def cancel(self):
        self.parent.event_generate("<<CorrectionCancel>>")
        self.num_label.configure(fg="white")
