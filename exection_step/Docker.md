# Dockerでパッケージ化

## 1.必要なライブラリのリスト
`app.py`と同じ場所に移動し、`requirements.txt`を作成し、以下のコードを貼り付ける。

```ruby:requirements.txt
pandas
langchain
langchain-community
langchain-core
langchain-openai
faiss-cpu
tiktoken
streamlit
```

## 2.箱の設計図
`Dockerfile`を作成し、以下のコードを貼り付ける。

```ruby:Dockerfile
# 1. ベースとなるOSとPythonのバージョンを指定
FROM python:3.11-slim
# 2. コンテナの中での作業ディレクトリを /app に設定
WORKDIR /app
# 3. 作ったリストを箱の中にコピー
COPY requirements.txt .
# 4. 箱の中でライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt
# 5. アプリのコードやCSVデータをすべて箱の中にコピー
COPY . .
# 6. Streamlitが使うポート番号「8501」を開ける宣言
EXPOSE 8501
# 7. コンテナを起動した時に自動で実行されるコマンド
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

## 3.コンテナを建てる
ターミナルで、以下のコマンドを実行する。
* `build`: 設計図を作る。
* `-t ---`: コンテナにタグをつける。
* `.`: ディレクトリ内の設計図やCSVファイルをすべて使う。

```
docker build -t cosme-app .
```

## 4.コンテナを動かす
ターミナルで、以下のコマンドを実行する。
* `run`: コンテナを起動する。
* `-p 8501:8501`: 8501番へのポートへのアクセスをコンテナにの8501番に繋ぐ。

```
docker run -p 8501:8501 cosme-app
```

## 5.ブラウザで確認
コマンドを実行すると、ターミナル上でStreamlitが起動したようなログが表示される。
ブラウザを開き、URL欄に **http://localhost:8501** を入力してアクセスする。