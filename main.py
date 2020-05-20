"""A project to track project management."""

import tkinter as tk

from datetime import datetime

WORKFLOWS = ['test']

class RecordSession:
    """Class for recording activity session."""

    def __init__(self, activity):
        self.activity = activity
        self.start = datetime.now()

    def endsession(self):
        self.end = datetime.now()


class MainWindow:
    """Class for the main GUI window."""

    def __init__(self):
        # Main window
        self.window = tk.Tk()

        # Top Message Frame
        self.message_frame = tk.Frame()
        self.message_frame.config(background="slate gray", height=10)

        # Button Frame
        self.button_frame = tk.Frame()
        self.button_frame.config(background="PaleGreen1")
        self.button_frame.columnconfigure(0, weight=1, minsize=75)
        self.button_frame.columnconfigure(1, weight=1, minsize=75)
        self.button_frame.columnconfigure(2, weight=1, minsize=75)
        self.button_frame.rowconfigure(0, weight=1, minsize=50)

        # Selection Frame
        self.selection_frame = tk.Frame()
        self.selection_frame.config(background="azure", height=30)

        # Initialize Top Message
        self.message = tk.Label(
            master=self.message_frame,
            text="Productivity tracker starting...",
            fg="black",
            bg="slate gray",
            width=40,
            font=("Roboto", 20)
        )
        self.message.pack()

        # Key buttons
        self.start_button = tk.Button(
            master=self.button_frame,
            text="Start",
            fg="green"
        )
        self.stop_button = tk.Button(
            master=self.button_frame,
            text="Stop",
            fg="red",
        )
        self.pause_button = tk.Button(
            master=self.button_frame,
            text="Pause",
            fg="Gold4",
        )

        # Slection options
        self.entry_label = tk.Label(
            master=self.selection_frame,
            text="Enter workflow name:",
            bg="azure",
            font=("Roboto", 16)
        )
        self.entry = tk.Entry(master=self.selection_frame, width=20)
        self.add_button = tk.Button(
            master=self.selection_frame,
            text="Add workflow",
            fg="green",
            command=self.add_new_workflow
        )
        self.workflow = tk.StringVar(self.window)
        self.workflow.set(WORKFLOWS[0])
        self.workflow_options = tk.OptionMenu(self.selection_frame, self.workflow, *WORKFLOWS)

        # Grid buttons and labels
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.pause_button.grid(row=0, column=2, padx=5, pady=5)
        self.entry_label.grid(row=0, column=0, padx=2, pady=2)
        self.entry.grid(row=1, column=0, padx=2, pady=2)
        self.add_button.grid(row=2, column=0, padx=2, pady=2)
        self.workflow_options.grid(row=0, column=1, padx=2, pady=2)

        # Pack frames
        self.message_frame.pack(fill=tk.X)
        self.button_frame.pack(fill=tk.X)
        self.selection_frame.pack(fill='both', expand=True)
        self.window.mainloop()

    def add_new_workflow(self):
        """Adds a new workflow to the list."""
        workflow = self.entry.get()
        WORKFLOWS.append(workflow)
        print(WORKFLOWS)
        self.entry.delete(0, tk.END)


def main():
    """Main function. This launched the GUI."""
    window = MainWindow()


if __name__ == '__main__':
    main()
