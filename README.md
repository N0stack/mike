# mike

Mike is calico cat called in Japanese.

This component is debeloped for n0stack networking.
All packets are processed by OpenFlow with Ryu SDN.

## Flow Model

![](docs/flow.png)

Packets are started from red round node.

## MVC
### Model

- N0stackObject (mike.lib.objects.n0stack_object)
  - Switches (mike.lib.objects.switches)
  - Ports (mike.lib.objects.ports)
  - SwitchLinks (mike.lib.objects.switche_links)
- service (mike.servces.service)
  - hub (mike.services.hub)

### View

- web (django)
- shell (django: manage.py)
- openflow (ryu)

### Controller

- 未定

## Author

- [@h-otter](https://github.com/h-otter)
