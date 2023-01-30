class Timeout(Exception):
    """
    This exception is raised when the command exceeds the defined timeout
    duration and the command is killed.
    """
    def __init__(self, cmd, timeout):
        self.cmd = cmd
        self.timeout = timeout

    def __str__(self):
        return "Command '%s' timed out after %d second(s)." % \
               (self.cmd, self.timeout)
