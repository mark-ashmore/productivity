"""Session recording module."""

from datetime import datetime

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
