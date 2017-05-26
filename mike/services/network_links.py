from mike.lib.mike_object import MikeObject
from mike.lib.objects.networks import ModelNetwork

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
        service: reference,
        network: reference,
        network2: reference,
    }
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=32, blank=True)
    service = models.UUIDField(null=False)  # controllerによってはforeignkey
    network = (
        models.ForeignKey(ModelNetwork, related_name="network_links", null=False),
        models.ForeignKey(ModelNetwork, related_name="network_links", null=False),
    )

    class Meta:
        unique_together = (('network', 'network2'))
        app_label = 'mike'

    def clean(self):
        # valid mac address
        pass

    # def clean_():

    def __unicode__(self):
        return self.uuid
