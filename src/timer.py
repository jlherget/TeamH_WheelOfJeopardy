from timeit import default_timer as timer

class Timer():
    """Generic timer class."""

    def __init__(self):
        self.start_time = 0
        self.end_time  = 0

    def start(self, duration):
        """Start the timer with specified duration in seconds."""
        self.start_time = timer()
        self.end_time   = self.start_time + duration
    
    def time_left(self):
        """Return the number of seconds remaining in the timer."""
        now = timer()
        return (self.end_time - now)

    def time_elapsed(self):
        """Return the number of seconds elapsed since the timer started."""
        now = timer()
        return (now - self.start_time)
