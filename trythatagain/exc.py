class CaughtException(Exception):
    def __init__(self, message, caught_exception):
        super(CaughtException, self).__init__(message)
        self.caught = caught_exception
