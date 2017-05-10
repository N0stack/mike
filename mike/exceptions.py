import logger


class ExceptionAlreadyExists(Exception):
    '''
    if the object already exists, this exception is raised
    '''
    def __init__(self, obj, service=None):
        self.obj = obj
        if service:
            self.service = service