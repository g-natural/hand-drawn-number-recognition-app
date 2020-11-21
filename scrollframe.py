import tkinter as tk
from tkinter import ttk

# couple a scroll bar to a frame
class ScrollFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="ns")
        scrollbar.grid(row=0, column=1, sticky="ns")


        self.bind('<Enter>', self._on_mouse_enter)
        self.bind('<Leave>', self._on_mouse_leave)

        self.canvas.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    # cross-platform mousewheel scrolling handler
    def _mouse_wheel(self, event):
        direction = 0
        if event.num == 5 or event.delta == -120:
            direction = 1  # scrolling "up"
        if event.num == 4 or event.delta == 120:
            direction = -1  # scrolling "down"
        self.canvas.yview_scroll(direction, "units")

    def _on_mouse_enter(self, event):
        self.bind_all("<Button-4>", self._mouse_wheel)
        self.bind_all("<Button-5>", self._mouse_wheel)

    def _on_mouse_leave(self, event):
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")


# def main():
#     root = tk.Tk()
#     scrollframe = ScrollFrame(root)

#     for i in range(50):
#         tk.Label(scrollframe.scrollable_frame, text=f"Sample scrolling label {i}").pack()

#     scrollframe.grid(row=0, column=0)

#     root.mainloop()

# main()
