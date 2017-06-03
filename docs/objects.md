# mike.lib.objects

- 完全に実態と一致するような状態を保つ

## mike.lib.objects.switch

```
{
    "uuid": UUID,
    "name": string,
    "port_id": uuid,
    "type": char[2], 'in' / 'ex' / 'ph'
    "datapath_id": integer,
    "services": manytomany reference,
    "ports": [
        reference,
    ],
    "links": [
        reference,
    ]
}
```

- APIを叩くことで各ホストにovsdbでスイッチを作成する
- internal / external / physicalの3種類のスイッチを区別
- servicesについては考え中

## mike.lib.objects.interface

- abstractクラス

## mike.lib.objects.port

```
{
    "uuid": UUID,
    "name": string,
    "number": integer,
    "switch": reference,
}
```

- ホストをつなぐ
- 基本的にVMを作成する際にはAPIを叩く必要はない
  - openflow側で生成されたことを認識できるため
  - MACアドレスの登録は `mike.services.hub` で

## mike.lib.objects.link

```
{
    "uuid": integer,
    "name": string,
    "number": integer,
    "switch": reference,
    "next_link": reference,
}
```

- internalとexternalスイッチをつなぐ
  - internalとinternalは禁止 (Modelの制約を追加済み)
- 現状はSwitchが作成された時点で自動的に生成される予定
  - APIでPOSTする必要はない
