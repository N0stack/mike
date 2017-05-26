from mike.lib.mike_object import MikeObject

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ryu.lib.ip import valid_ipv4
from uuid import uuid4


class ModelNetowrkLinks(models.Model):
    '''
    {
        id: UUID,
        name: string,
        host_id: reference,
        next_link: reference,
    }
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=32, blank=True)

    class Meta:
        app_label = 'mike'

    def clean(self):
        # valid mac address
        pass

    def __unicode__(self):
        return self.uuid
