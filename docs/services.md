# mike.services.service

- 抽象的なopenflowアプリケーション
- それぞれのハンドラが呼ばれる
- priorityを上げたうえでapply actionsでCONTROLLERを実行することで上位のプロトコルを問題なく実行
- serviceは `mike.lib.objects` をいじってはいけない
