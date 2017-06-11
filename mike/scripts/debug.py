def check_hub_table():
    from mike.services.hub import *
    t = ServiceHubTable.objects.all()
    for i in t:
        print("%s %s %s" % (i.hw_addr, i.port.name, i.floating))
