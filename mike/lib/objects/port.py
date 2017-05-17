from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mike.lib.objects.n0stack_object import N0stackObject
from mike.lib.objects.switch import Switch


class Port(N0stackObject):
    '''
    {
        "uuid": UUID,
        "name": string,
        "number": integer,
        "switch": reference,
    }
    '''
    name = models.CharField(max_length=16, null=False, blank=False)
    number = models.IntegerField(null=True)

    class Meta:
        unique_together = (('switch', 'number'))
        abstract = True

    def __unicode__(self):
        return self.uuid
