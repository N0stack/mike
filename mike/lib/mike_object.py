from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4


class UUIDObjectType(models.Model):
    '''
    {
        "id": integer,
        "name": string,
        "path": string,
        "type": 'n0stack', 'service',
    }
    '''

    UUID_OBJECT_TYPE = (
        (u'n0stack', 'n0stack objects'),  # n0stack objects
        (u'service', 'service objects'),  # service objects
    )

    name = models.CharField(max_length=16, null=False)
    path = models.CharField(max_length=64, null=False)
    type = models.CharField(max_length=8, null=False, editable=False, choices=UUID_OBJECT_TYPE)
    # priority = models.IntegerField()  # service priority

    class Meta:
        unique_together = (('name', 'path'))
        app_label = 'mike'

    def clean(self):
        try:
            __import__(self.path, fromlist=[self.name])
        except:
            raise ValidationError(_('cannot import ' + self.name + ' from ' + self.path))

    def __unicode__(self):
        return self.name


class UUIDObject(models.Model):
    '''
    {
        "uuid": UUID,
        "object_type": reference,
    }
    '''

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    object_type = models.ForeignKey(UUIDObjectType, related_name="instances", null=False, editable=False)

    class Meta:
        app_label = 'mike'

    def __unicode__(self):
        return self.uuid


class MikeObject(models.Model):
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
        super(MikeObject, self).save(*args, **kwargs)

def get_object_type(uuid):
    '''
    return UUIDObjectType
    '''
    return UUIDObject.objects.filter(uuid=uuid)[0].object_type
