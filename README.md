# 使い方

### まずは、仮想環境の設定

venvを作成する。

``python -m venv venv``

仮想環境に入る。

``source venv/bin/activate``

必要なライブラリをインストールする。

``pip install -r requirements.txt``

### diffを取得する
ターミナルで以下のコマンドを実行する。

``python output-diff.py``

対話型でスクリプトなので、下記のように使用する設定ファイルを選択する。
カーソルを移動させて、エンターキーを押すと選択できる。
設定ファイルについては、後述する。
```
[?] 使用する設定ファイルを選択してください:: ./.env/Fastener-EPU.txt
 > ./.env/A.txt
   ./.env/B.txt
```

次に、ブランチを選択する。
```
From https://dev.azure.com/xxx
 * branch            main       -> FETCH_HEAD
[?] 以下のブランチから選択してください::   origin/bug/myfix
   origin/HEAD -> origin/main
     origin/main
 >   origin/bug/myfix
```

既にリポジトリが存在する場合は、fetchしてpullするようになっている。
存在しない場合は、cloneするようになっている。

処理が完了したら、「差分を出力しました。」と表示され、カレントディレクトリに差分ファイルが出力されます。
差分ファイルの名前は、ブランチ名になります。

# 設定
.envファイルを作成し、以下のように設定する

```
.env
├── A.txt
└── B.txt
```


以下のような設定をする。gitのパスは端末によってインストール先が異なるので、適宜変更すること。
which gitで確認できる。

```
[Repository]
url=https://dev.azure.com/xxxx
password=xxx

[Git]
path=/usr/bin/git
```
