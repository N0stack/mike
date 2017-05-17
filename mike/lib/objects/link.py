from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mike.lib.objects.switch import Switch
from mike.lib.objects.port import Port


class Link(Port):
    '''
    {
        "uuid": integer,
        "name": string,
        "number": integer,
        "switch": reference,
        "next_link": reference,
    }
    '''
    switch = models.ForeignKey(Switch, related_name="links", null=False, editable=False)
    next_link = models.ForeignKey('self', null=False)

    class Meta:
        unique_together = (('switch', 'next_link'), ('switch', 'number'))

    def clean(self):
        if self.switch is self.next_link.switch:
            raise ValidationError(_('cannot link with same switch'))


# def create_link(switches):
#     if switches[0].host_id == switches[1].host_id:
#         raise Exception  # TODO: maybe this block will be changed when developing l2 tunneling

#     new_link1 = Link(name=link_switches[0].name,
#                                 number=link_switches[0].number,
#                                 switch=switches[0])
#     new_link2 = Link(name=link_switches[1].name,
#                                 number=link_switches[1].number,
#                                 next_link=new_link1,
#                                 switch=switches[1])
#     new_link1.next_link = new_link2
#     new_link1.save()
#     new_link2.save()
