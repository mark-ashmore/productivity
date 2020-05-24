"""A project to track project management."""

import threading

import tkinter as tk

from datetime import datetime

WORKFLOWS = ['Select workflow']

LOG = []

TICKER_RUNNING = False

COUNTER = 28800

def counter_fun(label):
    print('running ticker')
    def count():
        if TICKER_RUNNING:
            global COUNTER

            # To manage the intial delay.
            if COUNTER == 28800:
                display = 'Starting...'
            else:
                time_stamp = datetime.fromtimestamp(COUNTER)
                display = time_stamp.strftime('%H:%M:%S')
            label['text'] = display

            # Delays by 1000ms=1 seconds and call count again.
            label.after(1000, count)
            COUNTER += 1
            print('counting')
        else:
            print('not running')

    # Triggering the start of the counter.
    count()

class RecordSession:
    """Class for recording activity session."""

    def __init__(self, activity):
        self.activity = activity
        self.start = datetime.now()
        self.log = []
        self.session = 0
        self.status = 'started'

    def session_log(self):
        end = datetime.now()
        total_time = self.start - end
        session_num = str(self.session)
        self.log.append({
            'session number': session_num,
            'start time': self.start,
            'end time': end,
            'total time': total_time
        })
        self.session += 1
        self.status = 'logged'

    def add_session(self):
        self.start = datetime.now()
        self.status = 'started'

class MainWindow:
    """Class for the main GUI window."""

    def __init__(self):
        # Main window
        self.window = tk.Tk()

        # Top Message Frame
        self.message_frame = tk.Frame()
        self.message_frame.config(background='slate gray', height=10)

        # Ticker Frame
        # shows elapsed time
        # toggle off if you want
        self.ticker_frame = tk.Frame()
        self.ticker_frame.config(background='gray10')

        # Button Frame
        self.button_frame = tk.Frame()
        self.button_frame.config(background='PaleGreen1')
        self.button_frame.columnconfigure(0, weight=1, minsize=75)
        self.button_frame.columnconfigure(1, weight=1, minsize=75)
        self.button_frame.columnconfigure(2, weight=1, minsize=75)
        self.button_frame.rowconfigure(0, weight=1, minsize=50)

        # Selection Frame
        self.selection_frame = tk.Frame()
        self.selection_frame.config(background='azure', height=30)
        self.selection_frame.columnconfigure(0, weight=1, minsize=75)
        self.selection_frame.columnconfigure(1, weight=1, minsize=75)
        self.selection_frame.rowconfigure(0, weight=1, minsize=50)
        self.selection_frame.rowconfigure(1, weight=1, minsize=50)
        self.selection_frame.rowconfigure(2, weight=1, minsize=50)

        # Tracker Frame
        self.tracker_display_frame = tk.Frame()
        self.tracker_display_frame.config(
            background='khaki',
            height=70
        )

        # Initialize Top Message
        self.message = tk.Label(
            master=self.message_frame,
            text='Productivity tracker starting...',
            fg='black',
            bg='slate gray',
            width=40,
            font=('Roboto', 20)
        )
        self.message.pack()

        # Initialize Ticker Message
        self.ticker = tk.Label(
            master=self.ticker_frame,
            text='00:00:00',
            fg='white',
            bg='gray10',
            font=('Droid Sans Mono Dotted for Powerline Regular', 16)
        )

        # Key buttons
        self.start_button = tk.Button(
            master=self.button_frame,
            text='Start',
            fg='green',
            command=self.start_recording
        )
        self.stop_button = tk.Button(
            master=self.button_frame,
            text='Stop',
            fg='red',
            command=self.stop_recording,
            state='disabled'
        )
        self.pause_button = tk.Button(
            master=self.button_frame,
            text='Pause',
            fg='Gold4',
            command=self.pause_recording,
            state='disabled'
        )

        # Slection options
        self.entry_label = tk.Label(
            master=self.selection_frame,
            text='Enter workflow name:',
            bg='azure',
            font=('Roboto', 16)
        )
        self.entry = tk.Entry(master=self.selection_frame, width=20)
        self.add_button = tk.Button(
            master=self.selection_frame,
            text='Add workflow',
            fg='green',
            command=self.add_new_workflow
        )
        self.track_label = tk.Label(
            master=self.selection_frame,
            text='Workflow to track',
            bg='azure',
            font=('Roboto', 16),
            justify=tk.LEFT
        )
        self.workflow = tk.StringVar(self.window)
        self.workflow.set(WORKFLOWS[0])
        self.workflow_options = tk.OptionMenu(self.selection_frame, self.workflow, *WORKFLOWS)
        self.workflow_options.config(width=20, font=('Roboto', 16))
        self.select_button = tk.Button(
            master=self.selection_frame,
            text='Track workflow',
            fg='blue',
            command=self.get_selected_workflow
        )

        # Tracker display
        self.tracker_display = tk.Label(
            master=self.tracker_display_frame,
            text='Record display:',
            bg='khaki',
            font=('Roboto', 12)
        )

        # Grid buttons and labels
        self.ticker.pack()
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.pause_button.grid(row=0, column=2, padx=5, pady=5)
        self.entry_label.grid(row=0, column=0, padx=2, pady=2)
        self.entry.grid(row=1, column=0, padx=2, pady=2)
        self.add_button.grid(row=2, column=0, padx=2, pady=2)
        self.track_label.grid(row=0, column=1, padx=2, pady=2)
        self.workflow_options.grid(row=1, column=1, padx=2, pady=2)
        self.select_button.grid(row=2, column=1, padx=2, pady=2)
        self.tracker_display.pack()

        # Pack frames
        self.message_frame.pack(fill=tk.X)
        self.ticker_frame.pack(fill=tk.X)
        self.button_frame.pack(fill=tk.X)
        self.selection_frame.pack(fill='both', expand=True)
        self.tracker_display_frame.pack(fill='both', expand=True)
        self.window.mainloop()

    def add_new_workflow(self):
        """Adds a new workflow to the list."""
        workflow = self.entry.get()
        WORKFLOWS.append(workflow)
        print(WORKFLOWS)
        self.entry.delete(0, tk.END)
        self.workflow_options = tk.OptionMenu(
            self.selection_frame,
            self.workflow,
            *WORKFLOWS
        )
        self.workflow_options.config(width=20, font=('Roboto', 16))
        self.workflow_options.grid(row=1, column=1, padx=2, pady=2)
        self.message['text'] = "Adding " + workflow + " to workflow options."

    def get_selected_workflow(self):
        """Returns the workflow selected for tracking."""
        self.last_selection = self.workflow.get()
        self.message['text'] = 'Ready to track ' + self.last_selection

    def start_recording(self):
        """Kicks off a recording session for a workflow."""
        try:
            selection = self.last_selection
        except AttributeError:
            self.message['text'] = 'Please select "track workflow" before starting.'
        else:
            print(LOG)
            is_logged = False
            for a in LOG:
                if self.last_selection == a.activity:
                    a.add_session()
                    is_logged = True
                    break
                else:
                    continue
            if not is_logged:
                self.logged_selection = RecordSession(self.last_selection)
                LOG.append(self.logged_selection)
            self.message['text'] = 'Now tracking ' + self.last_selection + '...'
            global TICKER_RUNNING
            TICKER_RUNNING = True
            counter_fun(self.ticker)
            self.start_button['state'] = 'disabled'
            self.stop_button['state'] = 'normal'
            self.pause_button['state'] = 'normal'


    def pause_recording(self):
        """Pauses a recording session."""
        is_logged = False
        for a in LOG:
            if self.last_selection == a.activity:
                if a.status == 'started':
                    a.session_log()
                    self.message['text'] = 'Pausing ' +\
                                           self.last_selection + '...'
                    is_logged = True
                    self.update_display()
                    global TICKER_RUNNING
                    TICKER_RUNNING = False
                    self.start_button['state'] = 'normal'
                    self.stop_button['state'] = 'normal'
                    self.pause_button['state'] = 'disabled'
                    break
                else:
                    self.message['text'] = 'Recording hadn\'t started for ' +\
                                           self.last_selection + ' yet.'
            else:
                continue
        if not is_logged:
            self.message['text'] = 'Recording hadn\'t started for ' +\
                                   self.last_selection + ' yet.'

    def stop_recording(self):
        """Stops a recording session."""
        is_logged = False
        for a in LOG:
            if self.last_selection == a.activity:
                if a.status == 'started':
                    a.session_log()
                    self.message['text'] = 'Done recording ' +\
                                           self.last_selection
                    is_logged = True
                    self.update_display()
                    global TICKER_RUNNING
                    TICKER_RUNNING = False
                    self.start_button['state'] = 'normal'
                    self.stop_button['state'] = 'disabled'
                    self.pause_button['state'] = 'disabled'
                    global COUNTER
                    COUNTER = 28800
                    break
                else:
                    self.message['text'] = 'Recording hadn\'t started for ' +\
                                           self.last_selection + ' yet.'
            else:
                continue
        if not is_logged:
            self.message['text'] = 'Recording hadn\'t started for ' +\
                                   self.last_selection + ' yet.'
        self.workflow.set(WORKFLOWS[0])

    def update_display(self):
        """Update the trakcer display."""
        display = 'Record display:\n\n\nWORKFLOW\tSESSION\tSTART\tSTOP\n'
        for a in LOG:
            for x in a.log:
                display += a.activity + '\t' + x['session number'] + '\t' +\
                           x['start time'].strftime("%H:%M:%S") + '\t' +\
                           x['end time'].strftime("%H:%M:%S") + '\n'
        self.tracker_display['text'] = display
        self.tracker_display['justify'] = tk.LEFT
        # Add section for elapsed time as well

def main():
    """Main function. This launched the GUI."""
    window = MainWindow()


if __name__ == '__main__':
    main()
