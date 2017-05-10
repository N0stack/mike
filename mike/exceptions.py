

class ExceptionAlreadyExists(Exception):
    '''
    if the object already exists, this exception is raised
    '''

    # def __init__(self, exists_object, new_object=None, service=None):
    #     self.exists_object = exists_object
    #     self.new_object = new_object
    #     if service:
    #         self.service = service
    def __init__(self, message):
        pass
