from django.db import models

from mike.lib.uuid_object import UUIDObject, UUIDObjectType


class N0stackObject(models.Model):
    '''
    this is abstract class for n0stack object managed uuid
    uuid will be automaticaly seted
    '''

    uuid = models.UUIDField(primary_key=True, editable=False)

    class Meta:
        abstract = True
        app_label = 'mike'

    def save(self, *args, **kwargs):
        '''
        automatically set uuid and save for UUIDObject
        '''
        if self.uuid:
            new_object_type = UUIDObjectType.objects.filter(name=self.__class__.__name__)
            new_object = UUIDObject(object_type=new_object_type)
            new_object.save()
            self.uuid = new_object.uuid
        super(N0stackObject, self).save(*args, **kwargs)
