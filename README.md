# AI Cosmetics Advisor

## プロジェクトの概要
本プロジェクトは、ユーザーの肌の悩みや要望に合わせて、最適な化粧品を提案するRAGベースのAIチャットボットです。
Kaggleのコスメデータセット（Sephoraの成分データ）を活用し、データの前処理からAIモデルの組み込み、WebUIの作成、そしてAWSへのコンテナデプロイまでを構築しました。

## 使用データセット

本プロジェクトでは、Kaggleで公開されている以下のSephora（セフォラ）の製品・成分データを使用しています。

* **データセット名:** Sephora Products and Skincare Reviews
* **ソースリンク:** [Kaggle - Sephora Products and Skincare Reviews](https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews)

※データセットに含まれる約9,000件の製品データから、ブランド名、製品名、カテゴリー、価格、そして「成分情報（Ingredients）」を抽出・クレンジングし、RAGの知識ベースとして活用しています。

## 開発のステップ

本システムは、以下の5つのフェーズを経て構築されています。

### 1. データの前処理
* Kaggleから取得した非構造化テキストを含むコスメデータを読み込み。
* `pandas` を駆使し、欠損値の処理や、AIが文脈を理解しやすい「統合テキスト列（ブランド＋商品名＋成分）」の作成を実施。

### 2. RAGアーキテクチャの構築（LangChain / OpenAI）
* 処理済みのデータフレームをベクトル化し、FAISSを用いてローカルのベクトルデータベースを構築。
* 最新のLangChain Expression Language (LCEL) を採用し、古い `chains` モジュールの依存関係エラーを回避しつつ、シンプルで保守性の高いパイプラインを実装。
* OpenAI API (gpt-3.5-turbo) を用いて、美容のプロフェッショナルとして振る舞うプロンプトを設計。

### 3. Webアプリケーション化（Streamlit）
* コンソール上での対話から脱却し、誰もが直感的に操作できるチャットUIをStreamlitで構築。
* キャッシュ機能（`@st.cache_resource`）を活用し、ベクトルデータベースの読み込みを高速化。

### 4. コンテナ化（Docker）
* Mac / Windows / クラウドなどの環境差異（「私のPCでは動くのに」問題）をなくすため、Dockerによるコンテナ化を実施。
* 必要なライブラリ（`requirements.txt`）をまとめたスリムなPython環境を構築。

### 5. クラウドへのデプロイ（AWS ECS / Fargate）
* AWS CLIを用いて、ローカルのDockerイメージをAmazon ECR（コンテナレジストリ）へ安全にプッシュ。
* Mac (Apple Silicon) 特有のARM64アーキテクチャにAWS側の設定を合わせるトラブルシューティングを実施。
* Amazon ECS (Fargate) 上でタスクを実行し、セキュリティグループのインバウンドルール（ポート8501）を適切に開くことで、パブリックIP経由で全世界に公開。

## 技術スタック
* **言語**: Python 3.11
* **データ処理**: Pandas
* **AI / ML**: OpenAI API, LangChain (LCEL), FAISS, tiktoken
* **フロントエンド**: Streamlit
* **インフラ・環境**: Docker, AWS (ECR, ECS, Fargate, IAM)

## ディレクトリ構造

```text
cosme-rag-app/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── data/
│   └── sephora_website_dataset.csv  # Kaggleから取得した生データを格納
├── exection_step/
│   └── rag_bot_kaggle.ipynb
│   └── Streamlit.md
│   └── Docker.md
│   └── AWS.md
│   └── ci_cd.md
├── .gitignore
├── Dockerfile
├── README.md
├── app.py 
└── requirements.txt
```

## ローカル環境での動かし方

* リポジトリをクローン
```bash
git clone [https://github.com/ユーザー名/cosme-rag-app.git](https://github.com/ユーザー名/cosme-rag-app.git)
cd cosme-rag-app
