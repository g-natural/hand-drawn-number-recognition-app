import tkinter as tk
from tkinter import ttk
import scrollframe as sf


# couple button to label to view a node
class NodeViewer(tk.Frame):
    def __init__(self, parent, node_number):
        super().__init__(parent)
        self.parent = parent
        self.node_number = node_number
        self.button = tk.Button(self, text=node_number, padx=25,
                                pady=10, command=self.pressed)
        self.output_label = tk.Label(self)

        self.button.grid(row=0, column=0, sticky="w")
        self.output_label.grid(row=0, column=1)
        self.event = "<<ButtonPressed>>"

    def pressed(self):
        self.parent.event_generate(self.event,
                                   state=self.node_number)
    def set_output(self, value):
        self.output_label.config(text=" ->  " + str(value))

    def set_event(self, event_string):
        self.event = event_string


# couple a scroll bar to a list box
class ScrollBox(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.scrollbar = ttk.Scrollbar(self)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.columnconfigure(0, weight=1)

        self.listbox.grid(row=0, column=0, sticky="nesw")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def config(self, **options):
        self.listbox.config(**options)

    def clear(self):
        self.listbox.delete(0, tk.END)

    def insert(self, index, value):
        self.listbox.insert(index, value)


class NetworkViewer(tk.Toplevel):
    def __init__(self, parent, nnetwork):
        super().__init__(parent)

        self.title("Network Viewer")
        self.parent = parent
        self.nnet = nnetwork

        input_section = tk.Frame(self, padx=10)
        input_section.grid_rowconfigure(1, weight=1)
        input_section.grid_columnconfigure(0, weight=1)
        input_label = tk.Label(input_section, text="Input Vector")
        self.input_list = ScrollBox(input_section)
        input_label.grid(row=0, column=0, sticky="n")
        self.input_list.grid(row=1, column=0, sticky="nesw")
        input_section.grid(row=0, column=0, sticky="nesw")

        hw_section = tk.Frame(self, padx=10)
        hw_section.grid_rowconfigure(1, weight=1)
        hw_section.grid_columnconfigure(0, weight=1)
        self.hw_label = tk.Label(hw_section, text="Hidden Weights")
        self.hnode_weights = ScrollBox(hw_section)
        self.hw_label.grid(row=0, column=0, sticky="n")
        self.hnode_weights.grid(row=1, column=0, sticky="nesw")
        hw_section.grid(row=0, column=1, sticky="nesw")

        hnode_section = tk.Frame(self)
        hnode_section.grid_rowconfigure(1, weight=1)
        hnode_section.grid_columnconfigure(0, weight=1)
        hnode_section.grid(row=0, column=2, sticky="nesw")
        hnodes_label = tk.Label(hnode_section, text="Hidden Nodes")
        hnodes_label.grid(row=0, column=0, sticky="n")
        self.hnode_frame = sf.ScrollFrame(hnode_section)
        self.hnode_frame.grid(row=1, column=0, sticky="ns")
        self.hnode_frame.grid_columnconfigure(0, weight=1)
        self.hnode_list = self.hnode_frame.scrollable_frame
        self.hnode_viewers = []
        for i in range(self.nnet.hidden_ncount+1):
            nview = NodeViewer(self.hnode_list, i)
            nview.event = "<<HiddenPressed>>"
            nview.button.config(text=f"h{i}")
            nview.grid(row=i, column=0, sticky="w")
            self.hnode_viewers.append(nview)

        ow_section = tk.Frame(self, padx=10)
        ow_section.grid_rowconfigure(1, weight=1)
        ow_section.grid_columnconfigure(0, weight=1)
        self.outw_label = tk.Label(ow_section, text="Output Weights")
        self.outnode_weights = ScrollBox(ow_section)
        self.outw_label.grid(row=0, column=0, sticky="n")
        self.outnode_weights.grid(row=1, column=0, sticky="nesw")
        ow_section.grid(row=0, column=3, sticky="nesw")

        output_section = tk.Frame(self)
        output_section.grid_rowconfigure(1, weight=1)
        output_section.grid_columnconfigure(0, weight=1)
        output_section.grid(row=0, column=4, sticky="nesw")
        outnode_label = tk.Label(output_section, text="Output Nodes")
        outnode_label.grid(row=0, column=0, sticky="n")
        self.outnode_frame = sf.ScrollFrame(output_section)
        self.outnode_frame.grid(row=1, column=0, sticky="nesw")
        self.outnode_frame.grid_columnconfigure(0, weight=1)
        self.outnode_list = self.outnode_frame.scrollable_frame
        self.outnode_viewers = []
        for i in range(self.nnet.output_ncount):
            nview = NodeViewer(self.outnode_list, i)
            nview.event = "<<OutputPressed>>"
            nview.button.config(text=f"o{i}")
            nview.grid(row=i, column=0, sticky="w")
            self.outnode_viewers.append(nview)

        self.bind("<<HiddenPressed>>", self.view_hweights)
        self.bind("<<OutputPressed>>", self.view_outweights)

        # initialize weight lists to h1 and o0
        self.current_hweights = -1
        self.current_oweights = -1
        self.event_generate("<<HiddenPressed>>", state=1)
        self.event_generate("<<OutputPressed>>", state=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=2)

        self.grid_rowconfigure(0, weight=1)
        
        self.protocol("WM_DELETE_WINDOW", self.exit_button)

    def update_input(self, input_vector):
        self.input_list.clear()
        # set implicit input node (i0) which is always 1
        self.input_list.insert(0, f"i0: 1")

        for i in range(len(input_vector)):
            self.input_list.insert(i+1, f"i{i+1}: {input_vector[i]}")

        hlayer_output = self.nnet._CRNNetwork__layer_output(input_vector,
                        self.nnet.hidden_weights, self.nnet.hiddenl_bias)

         # set value for implicit hnode (h0)
        self.hnode_viewers[0].set_output(1)
        for i in range(len(hlayer_output)):
            self.hnode_viewers[i+1].set_output(hlayer_output[i])
       
        output_vector = self.nnet._CRNNetwork__layer_output(hlayer_output,
                        self.nnet.output_weights, self.nnet.outputl_bias)

        for i in range(len(output_vector)):
            self.outnode_viewers[i].set_output(output_vector[i])

    def view_hweights(self, event):
        if(event.state == self.current_hweights):
            return
        ypos, yvis = self.hnode_weights.listbox.yview()
        self.hnode_weights.clear()

        if(event.state == 0):
            self.hnode_weights.insert(0, "Implicit node h0")
            self.hnode_weights.insert(1, "has no weights")
        else:
            # set h0 weight
            self.hnode_weights.insert(0,
                f"w0: {self.nnet.hiddenl_bias[event.state-1]}")
            for i in range(1, len(self.nnet.hidden_weights)+1):
                self.hnode_weights.insert(i,
                f"w{i}: {self.nnet.hidden_weights[i-1][event.state-1]}")

            self.hnode_weights.listbox.yview_moveto(ypos)

        self.hw_label.config(text=f"Hidden Weights - [h{event.state}]")
        self.current_hweights = event.state

    def view_outweights(self, event):
        if(event.state == self.current_oweights):
            return
        ypos, yvis = self.outnode_weights.listbox.yview()
        self.outnode_weights.clear()
        # set h0 weight
        self.outnode_weights.insert(0,
            f"w0: {self.nnet.outputl_bias[event.state]}")
        for i in range(1, len(self.nnet.output_weights)+1):
            self.outnode_weights.insert(i,
            f"w{i}: {self.nnet.output_weights[i-1][event.state]}")

        self.outnode_weights.listbox.yview_moveto(ypos)
        self.outw_label.config(text=f"Output Weights - [o{event.state}]")
        self.current_oweights = event.state

    def exit_button(self):
        self.parent.event_generate("<<NetViewExit>>")
