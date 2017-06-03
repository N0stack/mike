# mike.services.service

- 抽象的なopenflowアプリケーション
- それぞれのハンドラが呼ばれる
- priorityを上げたうえでapply actionsでCONTROLLERを実行することで上位のプロトコルを問題なく実行
- serviceは `mike.lib.objects` をいじってはいけない

## mike.services.hub

```
{
    "id": integer,
    "hub": reference,
    "port": reference,
    "hw_addr": char[17],
    "float": boolean,
}
```

- L2ネットワークと同義
  - 1つhubが1つのL2ネットワークを意味する
  - tunnelingも内包する予定

### `/v1/services/hub/(?P<hub_uuid>)`

- GET
- PUT
- DELETE
  * どういう感じがいいんだろ

- POST

```
{
    "hub": reference,
    "port": reference,
    "hw_addr": char[17],
}
```

- 固定MACアドレスを登録
- `float = false`
- mqを通じてopenflowからフローを送信
