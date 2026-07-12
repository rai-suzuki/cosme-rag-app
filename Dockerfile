FROM python:3.11-slim

# 作業フォルダを /app に設定
WORKDIR /app

# コンテナ内でライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコード等を全てコピー
COPY . .

# ポート番号
EXPOSE 8501

# コンテナ起動時の実行コマンド
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]