# 使い方

### まずは、仮想環境の設定

venv を作成する。

`python -m venv venv`

仮想環境に入る。

`source venv/bin/activate`

必要なライブラリをインストールする。

`pip install -r requirements.txt`

### diff を取得する

ターミナルで以下のコマンドを実行する。

`python output-diff.py`

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

既にリポジトリが存在する場合は、fetch して pull するようになっている。
存在しない場合は、clone するようになっている。

もし、リポジトリーの内容が更新されていない場合は、
tmp_clone ディレクトリーを削除してから再度実行してください。

```
[?] リポジトリーが存在します。fetch して pull しますか？::  y
```

処理が完了したら、「差分を出力しました。」と表示され、カレントディレクトリに差分ファイルが出力されます。
差分ファイルの名前は、ブランチ名になります。

# 設定

.env ファイルを作成し、以下のように設定する

```
.env
├── A.txt
└── B.txt
```

以下のような設定をする。git のパスは端末によってインストール先が異なるので、適宜変更すること。
which git で確認できる。

```
[Repository]
url=https://dev.azure.com/xxxx
password=xxx

[Git]
path=/usr/bin/git
```

# GPT Code Review Script

このスクリプトは、指定されたテキストファイル内のコードを読み込み、ChatGPT API を使用してコードレビューを行います。レビューの結果は別のテキストファイルに保存されます。

## 前提条件

- Python 3.6 以上がインストールされていること。
- `requests` と `inquirer` ライブラリがインストールされていること。これらは `pip` を使用してインストールできます。

  ```bash
  pip install requests inquirer
  ```

- OpenAI の API キーが必要です。API キーは [OpenAI のウェブサイト](https://openai.com/) から取得できます。

## 使い方

1. まず、スクリプトを実行するためには環境変数 `OPENAI_API_KEY` に API キーを設定する必要があります。

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

このスクリプトは、指定されたテキストファイルに書かれたコードを ChatGPT API に送信し、得られたレビューを保存します。
API の使用には費用がかかる場合がありますので、OpenAI の料金体系を事前に確認してください。

# summarize_contents について

## 概要

summarize_contents.py は、指定されたディレクトリ内のファイルとサブディレクトリをスキャンし、それらの内容を概要としてテキストファイルにまとめる Python スクリプトです。特定のパターンにマッチするファイルやディレクトリを除外し、バイナリファイルを識別して無視する機能を持っています。

## 使用方法

コマンドラインから以下のようにスクリプトを実行します:

```bash
python summarize_contents.py --path <ディレクトリのパス> [--include_ignore <True/False>] [--output_file <出力ファイル名>]
```

--path: 概要を作成するディレクトリのパス（必須）。
--include_ignore: .gitignore ファイルのパターンを考慮に入れるかどうか（オプション、デフォルトは False）。
--output_file: 出力ファイルの名前（オプション、デフォルトは summary.txt）。

ディレクトリのスキャン: 指定されたディレクトリ内の全ファイルとサブディレクトリを再帰的にスキャンします。
除外パターン: .gitignore や EXCLUDE_PATTERNS に定義されたパターンにマッチするファイルやディレクトリは処理されません。
バイナリファイルの検出: ファイルがバイナリかどうかをチェックし、バイナリファイルは無視されます。

## 詳細

デフォルト除外パターン: EXCLUDE_PATTERNS には、デフォルトで無視されるべきファイルやディレクトリのパターンが設定されています（例：node_modules/\*、venv）。

出力形式
summary.txt: スクリプトは summary.txt というファイルに結果を出力します。各ファイルのパスとその内容が含まれます。
エラーハンドリング
バイナリファイルとデコードエラー: バイナリファイルやデコードできないファイルは、エラーメッセージとともに記録されます。

依存関係

このスクリプトは Python 3.x を使用し、標準ライブラリのみに依存しています。外部ライブラリは必要ありません。

使用例

ディレクトリ /Users/takumi/Documents/my_project の内容を概要化し、.gitignore ファイルを考慮に入れる例：

```
python summarize_contents.py --path /Users/takumi/Documents/my_project --include_ignore True
```

このコマンドは、指定されたディレクトリの内容をスキャンし、summary.txt ファイルにその概要を出力します。
