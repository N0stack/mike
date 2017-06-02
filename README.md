# mike

Mike is calico cat called in Japanese.

This component is debeloped for n0stack networking.
This is web api as NorthBound interface of managing network.

## Flow Model

![](docs/flow.png)

- Packets are started from red round node
- blue block means packetin

## architecture

```
    ||
    || HTTP
    \/
 +------+  +-----------------+
 REST API  OpenFlow Controller
 +------+  +-----------------+
 /\    ||    /\ /\   /\ ||
 ||    ||    || ||   || ||
 ||    ||    || ||   || ||
 |============| ||   || ||
 ||    ||       ||   || ||
 \/    \/       ||   || ||
+---+  ++       ||   || ||
RDBMS  MQ========|   || ||
+---+  ++            || ||
            Openflow || || ovsdb
                     \/ \/
                 +----------+
                 Open vSwitch
                 +----------+
```

## Author

- [@h-otter](https://github.com/h-otter)
