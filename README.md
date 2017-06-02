# mike

Mike is calico cat called in Japanese.

This component is debeloped for n0stack networking.
This is web api as NorthBound interface of managing network.

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
