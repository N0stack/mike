from abc import ABCMeta, abstractmethod


class N0stackObject(metaclass=ABCMeta):
    '''
    this is abstract class for n0stack object managed uuid
    object_model must be overrided with django ORM model
    '''

    object_model = None

    @abstractmethod
    @classmethod
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
        object_model.objects.all().filter(
            uuid__in=uuids
        )[0].delete()

    @classmethod
    def get_from_uuids(cls, uuids):
        '''
        get model from uuids
        prams uuid: array
        return queries: array
        '''
        return object_model.objects.all().filter(
            uuid__in=uuids
        )

