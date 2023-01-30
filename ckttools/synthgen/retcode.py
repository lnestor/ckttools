class Retcode(Exception):
    """
    This exception is raise when a command exits with a non-zero exit status.
    """
    def __init__(self, cmd, retcode, output=None):
        self.cmd = cmd
        self.retcode = retcode
        self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % \
               (self.cmd, self.returncode)
