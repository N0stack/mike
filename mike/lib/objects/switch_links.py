from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mike.lib.objects.n0stack_object import N0stackObject
from mike.lib.objects.switches import Switch


class SwitchLink(N0stackObject):
    '''
    {
        "uuid": integer,
        "name": string,
        "number": integer,
        "next_link": reference,
        "switch": reference,
    }
    '''
    name = models.CharField(max_length=32, null=False)
    number = models.IntegerField(null=False)
    switch1 = models.ForeignKey(Switch, related_name="switch_links", null=False)
    switch2 = models.ForeignKey(Switch, related_name="switch_links", null=False)

    class Meta:
        unique_together = (('switch1', 'switch2'))
        app_label = 'mike'

    def clean(self):
        if self.switch1 is self.switch2:
            raise ValidationError(_('cannot link with same switch'))


# def create_switch_link(switches):
#     if switches[0].host_id == switches[1].host_id:
#         raise Exception  # TODO: maybe this block will be changed when developing l2 tunneling

#     new_link1 = SwitchLink(name=link_switches[0].name,
#                                 number=link_switches[0].number,
#                                 switch=switches[0])
#     new_link2 = SwitchLink(name=link_switches[1].name,
#                                 number=link_switches[1].number,
#                                 next_link=new_link1,
#                                 switch=switches[1])
#     new_link1.next_link = new_link2
#     new_link1.save()
#     new_link2.save()
