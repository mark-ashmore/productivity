"""A project to track project management."""

import pickle
import pytz
import threading
import tkinter as tk

from datetime import datetime

DEFAULT_WORKFLOWS = ['Select workflow']

try:
    WORKFLOWS = pickle.load(open('session_workflows.p', 'rb'))
except:
    WORKFLOWS = DEFAULT_WORKFLOWS

LOG = []

TICKER_RUNNING = False

IS_PAUSED = False

NEW_SELECT_NEEDED = True

COUNTER = 28800

NO_LIVE_REPORT = True

def counter_fun(label):
    def count():
        if TICKER_RUNNING:
            global COUNTER

            # To manage the intial delay.
            if COUNTER == 28800:
                display = 'Starting...'
            else:
                time_stamp = datetime.fromtimestamp(COUNTER, tz=pytz.timezone('US/Pacific'))
                display = time_stamp.strftime('%H:%M:%S')
            label['text'] = display

            # Delays by 1000ms=1 seconds and call count again.
            label.after(1000, count)
            COUNTER += 1

    # Triggering the start of the counter.
    count()

class RecordSession:
    """Class for recording activity session."""

    def __init__(self, activity):
        self.activity = activity
        self.start = datetime.now()
        self.log = []
        self.session = 1
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
        self.window.title('Mark\'s Productivity Tracker')

        # Top Message Frame
        self.message_frame = tk.Frame()
        self.message_frame.config(background='PaleGreen1', height=10)

        # Ticker Frame
        # shows elapsed time
        # toggle off if you want
        self.ticker_frame = tk.Frame()
        self.ticker_frame.config(background='gray10')

        # Button Frame
        self.button_frame = tk.Frame()
        self.button_frame.config(background='slate gray')
        self.button_frame.columnconfigure(0, weight=1, minsize=35)
        self.button_frame.columnconfigure(1, weight=1, minsize=35)
        self.button_frame.columnconfigure(2, weight=1, minsize=35)
        self.button_frame.rowconfigure(0, weight=1, minsize=30)

        # Selection Frame
        self.selection_frame = tk.Frame()
        self.selection_frame.config(background='white', height=20)
        self.selection_frame.columnconfigure(0, weight=1, minsize=35)
        self.selection_frame.rowconfigure(0, weight=1, minsize=30)
        self.selection_frame.rowconfigure(1, weight=1, minsize=30)
        self.selection_frame.rowconfigure(2, weight=1, minsize=30)

        # Tracker Frame
        self.tracker_display_frame = tk.Frame()
        self.tracker_display_frame.config(
            background='white',
            height=30,
        )

        # Initialize Top Message
        self.message = tk.Label(
            master=self.message_frame,
            text='Productivity tracker is ready',
            fg='black',
            bg='PaleGreen1',
            width=35,
            font=('Roboto', 16)
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
        self.track_label = tk.Label(
            master=self.selection_frame,
            text='Workflow to track',
            bg='white',
            font=('Roboto', 16),
            justify=tk.LEFT
        )
        self.workflow = tk.StringVar(self.window)
        global WORKFLOWS
        self.workflow.set(WORKFLOWS[0])
        self.workflow_options = tk.OptionMenu(self.selection_frame, self.workflow, *WORKFLOWS)
        self.workflow_options.config(width=15, font=('Roboto', 16))
        self.select_button = tk.Button(
            master=self.selection_frame,
            text='Track workflow',
            fg='blue',
            command=self.get_selected_workflow
        )
        self.add_new_button = tk.Button(
            master=self.selection_frame,
            text='Add new workflow',
            fg='green',
            command=self.add_new_workflow
        )

        # Tracker display
        self.tracker_display = tk.Label(
            master=self.tracker_display_frame,
            text='Record will display here',
            bg='white',
            font=('Roboto', 12)
        )

        # Grid buttons and labels
        self.ticker.pack()
        self.start_button.grid(row=0, column=0, padx=2, pady=2)
        self.stop_button.grid(row=0, column=1, padx=2, pady=2)
        self.pause_button.grid(row=0, column=2, padx=2, pady=2)
        self.track_label.grid(row=0, column=0, padx=2, pady=2)
        self.workflow_options.grid(row=1, column=0, padx=2, pady=2)
        self.select_button.grid(row=2, column=0, padx=2, pady=2)
        self.add_new_button.grid(row=3, column=0, padx=2, pady=2)
        self.tracker_display.pack(fill=tk.X)

        # Pack frames
        self.message_frame.pack(fill=tk.X)
        self.ticker_frame.pack(fill=tk.X)
        self.button_frame.pack(fill=tk.X)
        self.selection_frame.pack(fill='both', expand=True)
        self.tracker_display_frame.pack(fill='both', expand=True)
        self.window.mainloop()

    def _destory_new_workflow(self):
        self.new_workflow = self.entry.get()
        global WORKFLOWS
        WORKFLOWS.append(self.new_workflow)
        self.workflow_options = tk.OptionMenu(
            self.selection_frame,
            self.workflow,
            *WORKFLOWS
        )
        self.workflow_options.config(width=15, font=('Roboto', 16))
        self.workflow_options.grid(row=1, column=0, padx=2, pady=2)
        self.message['text'] = self.new_workflow + ' added to workflow options'
        self.message['bg'] = 'pale green'
        self.add_workflow_window.destroy()
        pickle.dump(WORKFLOWS, open('session_workflows.p', 'wb'))

    def add_new_workflow(self):
        """Adds a new workflow to the list."""

        # New Window to accept workflow addition
        self.add_workflow_window = tk.Tk()
        self.add_workflow_window.title('Add a workflow')

        # New Frame for addtion
        self.add_workflow_frame = tk.Frame(self.add_workflow_window)
        self.add_workflow_frame.config(background='white')

        # Entry options
        self.entry_label = tk.Label(
            master=self.add_workflow_frame,
            text='Enter workflow name:',
            bg='white',
            font=('Roboto', 16)
        )
        self.entry = tk.Entry(master=self.add_workflow_frame, width=20)
        self.add_button = tk.Button(
            master=self.add_workflow_frame,
            text='Add workflow',
            fg='green',
            command=self._destory_new_workflow
        )
        self.entry_label.grid(row=0, column=0, padx=2, pady=2)
        self.entry.grid(row=1, column=0, padx=2, pady=2)
        self.add_button.grid(row=2, column=0, padx=2, pady=2)
        self.add_workflow_frame.pack(fill='both', expand=True)

    def get_selected_workflow(self):
        """Returns the workflow selected for tracking."""
        if self.workflow.get() == 'Select workflow':
            self.message['text'] = 'Please select a workflow to start.'
            self.message['bg'] = 'salmon'
        else:
            self.last_selection = self.workflow.get()
            self.message['text'] = 'Ready to track ' + self.last_selection
            self.start_button['state'] = 'normal'
            self.message['bg'] = 'PaleGreen1'
            global NEW_SELECT_NEEDED
            NEW_SELECT_NEEDED = False

    def start_recording(self):
        """Kicks off a recording session for a workflow."""
        try:
            selection = self.last_selection
        except AttributeError:
            self.message['text'] = 'Please select "track workflow" before starting.'
            self.message['bg'] = 'salmon'
        else:
            global NEW_SELECT_NEEDED
            if NEW_SELECT_NEEDED:
                self.message['text'] = 'Please select a workflow to start.'
            else:
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
                self.message['bg'] = 'PaleGreen1'
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
                    self.message['bg'] = 'goldenrod'
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
                    self.message['bg'] = 'salmon'
            else:
                continue
        if not is_logged:
            self.message['text'] = 'Recording hadn\'t started for ' +\
                                   self.last_selection + ' yet.'
            self.message['bg'] = 'salmon'
        global IS_PAUSED
        IS_PAUSED = True

    def stop_recording(self):
        """Stops a recording session."""
        is_logged = False
        global IS_PAUSED
        if IS_PAUSED:
            self.message['text'] = 'Done recording ' +\
                                   self.last_selection
            self.message['bg'] = 'pale green'
            self.stop_button['state'] = 'disabled'
            IS_PAUSED = False
        else:
            for a in LOG:
                if self.last_selection == a.activity:
                    if a.status == 'started':
                        a.session_log()
                        self.message['text'] = 'Done recording ' +\
                                               self.last_selection
                        self.message['bg'] = 'pale green'
                        is_logged = True
                        self.update_display()
                        global TICKER_RUNNING
                        TICKER_RUNNING = False
                        self.start_button['state'] = 'disabled'
                        self.stop_button['state'] = 'disabled'
                        self.pause_button['state'] = 'disabled'
                        global COUNTER
                        COUNTER = 28800
                        break
                    else:
                        self.message['text'] = 'Recording hadn\'t started for ' +\
                                               self.last_selection + ' yet.'
                        self.message['bg'] = 'salmon'
                else:
                    continue
            if not is_logged:
                self.message['text'] = 'Recording hadn\'t started for ' +\
                                       self.last_selection + ' yet.'
                self.message['bg'] = 'salmon'
        global WORKFLOWS
        self.workflow.set(WORKFLOWS[0])
        global NEW_SELECT_NEEDED
        NEW_SELECT_NEEDED = True

    def workflow_report(self):
        """Displays a window with a full workflow report."""

        # New Window for workflow report
        self.workflow_report_window = tk.Tk()
        self.workflow_report_window.title('Workflow Report')

        # New Frame for addtion
        self.workflow_report_frame = tk.Frame(self.workflow_report_window)
        self.workflow_report_frame.config(background='white')

        # Entry options
        self.report_label = tk.Label(
            master=self.workflow_report_frame,
            text='Workflow Report:',
            bg='white',
            font=('Roboto', 16)
        )
        self.report_label.grid(row=0, column=0, padx=2, pady=2)
        self.workflow_report_frame.pack(fill='both', expand=True)

    def live_report_pack(self):
        """Set up live report display."""
        # Add button to generate a report
        self.show_full_report = tk.Button(
            master=self.tracker_display_frame,
            text='Show full report',
            fg='black',
            command=self.workflow_report
        )
        self.show_full_report.pack(side='bottom')
        self.tracker_display['state'] = 'disabled'

        def onFrameConfigure(canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox('all'))
        self.canvas = tk.Canvas(
            self.tracker_display_frame,
            borderwidth=2,
            bg='khaki',
            relief='sunken',
            highlightthickness=0
        )
        self.live_report_frame = tk.Frame(
            self.canvas,
            bg='khaki'
        )
        self.vsb = tk.Scrollbar(
            self.tracker_display_frame,
            orient='vertical',
            command=self.canvas.yview
        )
        self.vsb.config(bg='khaki')
        self.vsb.pack(side='right', fill=tk.Y)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((4,4), window=self.live_report_frame, anchor='nw')
        self.live_report_frame.bind('<Configure>', lambda event, canvas=self.canvas: onFrameConfigure(self.canvas))
        self.canvas.configure(yscrollcommand=self.vsb.set)
        global NO_LIVE_REPORT
        NO_LIVE_REPORT = False

    def update_display(self):
        """Update the trakcer display."""
        if NO_LIVE_REPORT:
            self.live_report_pack()
        header = ['WORKFLOW', 'SESSION', 'START', 'STOP']
        rows = [header]
        for a in LOG:
            for x in a.log:
                row = [
                    a.activity,
                    x['session number'],
                    x['start time'].strftime('%H:%M:%S'),
                    x['end time'].strftime('%H:%M:%S')
                ]
                rows.append(row)
        total_rows = len(rows)

        # Creating table
        for i in range(total_rows):
            for j in range(4):

                self.live_report_frame.columnconfigure(j, weight=0, minsize=90)
                self.live_report_frame.rowconfigure(i, weight=0, minsize=10)
                self.e = tk.Label(master=self.live_report_frame,
                                  bg='khaki',
                                  font=('Roboto', 12),
                                  text=rows[i][j]
                )

                self.e.grid(row=i, column=j, sticky='w')

        self.tracker_display['text'] = 'Record'



def main():
    """Main function. This launched the GUI."""
    window = MainWindow()


if __name__ == '__main__':
    main()
