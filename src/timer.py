from timeit import default_timer as timer

class Timer():

    def __init__(self):
        self.endTime = 0

    def start(self, duration):
        """Start the timer."""
        self.endTime = timer() + duration
    
    def time_left(self):
        """Return the number of seconds remaining in the timer."""
        now = timer()
        return (self.endTime - now)