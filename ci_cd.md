# CI/CDパイプラインの構築

## CI/CDとは
人間が手作業で行なっていたテストやデプロイの作業を自動化する仕組み。
* CI(Continuous Integration: 継続的統合): Githubにプッシュしたと同時に、「エラーがないか」「APIキーが漏れていないか」などのテストを実行し、問題なければ自動でDockerイメージを建てる工程。
* CD(Continuous Delivery/Deployment: 継続的配送/配備): CIで作られたDockerイメージを自動でAWS（ECR）に送り、ECSのタスクを最新版に切り替える工程。

## ECRに倉庫を作る
ターミナルで、以下のコマンドを実行する。

```
aws ecr create-repository --repository-name cosme-rag-app-repo
```

## Github Actionsの準備
Github上に自動化の設計図を作る。
ターミナルで、以下のコマンドを順番に実行する。

```
# 1. プロジェクトのなかに「.github」というフォルダを作り、そのなかにさらに「workflows」というフォルダを作る
mkdir -p .github/workflows

# 2. そのなかに「deploy.yml」という空の設計図ファイルを作る
touch .github/workflows/deploy.yml
```

### 設計図（deploy.yml）の記述

### Githubにキーを登録する
1. 任意のリポジトリを開く。
2. 上部メニューの「Setting」をクリックする。
3. 左側のメニューの「Security」の中の「Secrets and variables」>「Actions」をクリックする。
4. 右上の「New repository secret」をクリックする。
5. 鍵を１つずつ登録する。
 * 1つ目:
  * Name: AWS_ACCESS_KEY_ID
  * Secret: (あなたのAWSアクセスキー)
 * 2つ目:
  * Name: AWS_SECRET_ACCESS_KEY
  * Secret: (あなたのAWSシークレットアクセスキー)

* あとはpushすればECR上に倉庫が常に更新される状態で作成される。実行は`AWS.md`の「クラスターの作成」に沿って行う事ができる。