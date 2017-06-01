from django.db import models

from mike.lib.objects.interface import Interface
from mike.lib.objects.switch import Switch


class Port(Interface):
    '''
    {
        "uuid": UUID,
        "name": string,
        "number": integer,
        "switch": reference,
    }
    '''
    switch = models.ForeignKey(Switch, related_name="ports", null=False, editable=False)
