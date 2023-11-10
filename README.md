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

# GPT Code Review Script

このスクリプトは、指定されたテキストファイル内のコードを読み込み、ChatGPT APIを使用してコードレビューを行います。レビューの結果は別のテキストファイルに保存されます。

## 前提条件

- Python 3.6以上がインストールされていること。
- `requests` と `inquirer` ライブラリがインストールされていること。これらは `pip` を使用してインストールできます。

    ```bash
    pip install requests inquirer
    ```

- OpenAIのAPIキーが必要です。APIキーは [OpenAIのウェブサイト](https://openai.com/) から取得できます。

## 使い方

1. まず、スクリプトを実行するためには環境変数 `OPENAI_API_KEY` にAPIキーを設定する必要があります。

- **Linux/MacOS**:

  ```bash
  export OPENAI_API_KEY='your_api_key'
  ```

- **Windows**:

  ```cmd
  set OPENAI_API_KEY=your_api_key
  ```

2. スクリプトを実行するディレクトリにレビュー対象のテキストファイル（`.txt` 形式）を配置してください。

3. スクリプトを実行します。

```bash
python gpt-code-review.py
```

4. プロンプトが表示されたら、レビューするファイルを選択します。

5. レビューの結果は ./output ディレクトリ内に保存されます。

## 注意
このスクリプトは、指定されたテキストファイルに書かれたコードをChatGPT APIに送信し、得られたレビューを保存します。
APIの使用には費用がかかる場合がありますので、OpenAIの料金体系を事前に確認してください。
