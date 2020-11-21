import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")))

# cross-platform mousewheel scrolling handler
def mouse_wheel(event):
    direction = 0
    if event.num == 5 or event.delta == -120:
        direction = 1  # scrolling "up"
    if event.num == 4 or event.delta == 120:
        direction = -1  # scrolling "down"
    canvas.yview_scroll(direction, "units")

def on_mouse_enter(event):
    container.bind_all("<Button-4>", mouse_wheel)
    container.bind_all("<Button-5>", mouse_wheel)

def on_mouse_leave(event):
    container.unbind_all("<Button-4>")
    container.unbind_all("<Button-5>")


container.bind('<Enter>', on_mouse_enter)
container.bind('<Leave>', on_mouse_leave)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set,
                 scrollregion="0 0 0 %s" % scrollable_frame.winfo_height())

for i in range(50):
    ttk.Label(scrollable_frame, text=f"Sample scrolling label {i}").pack()

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()

# useful links
# https://stackoverflow.com/questions/5612237/inserting-a-button-into-a-tkinter-listbox-on-python
# https://blog.tecladocode.com/tkinter-scrollable-frames/
# https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar


