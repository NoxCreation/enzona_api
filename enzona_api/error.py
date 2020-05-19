
class EnzonaError(ValueError):
    def __init__(self, message, *args):
        super(EnzonaError, self).__init__(message, *args)