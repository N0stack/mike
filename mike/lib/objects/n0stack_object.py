from abc import ABCMeta, abstractmethod


class N0stackObject(metaclass=ABCMeta):
    '''
    this is abstract class for n0stack object managed uuid
    object_model must be overrided with django ORM model
    '''

    model = None

    @classmethod
    @abstractmethod
    def add(cls, *args, **kwargs):
        '''
        add new the object
        '''
        pass

    @classmethod
    def delete(cls, uuids):
        '''
        delete the object for mike base system
        prams (uuid: array)
        return queries: array
        '''
        cls.model.objects.filter(uuid__in=uuids).delete()

    @classmethod
    def get_from_uuids(cls, uuids):
        '''
        get model from uuids
        prams uuid: array
        return queries: array
        '''
        return cls.model.objects.filter(uuid__in=uuids)
