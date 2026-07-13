# AWSへデプロイ

## アカウント準備とIAMユーザーの作成
1. AWS公式サイトからアカウントを作成して、ログインする。
2. 画面上部の検索窓で「**IAM**」と検索し、ダッシュボードを開く。
3. 左側のメニューバーから、「IAMユーザー」を開き、「ユーザーの作成」をクリックする。
4. ユーザー名を入力して「次へ」を押す。
5. 「許可のオプション」で「ポリシーを直接アタッチする」を選び、リストから`AdministratorAccess`（管理者権限）にチェックを入れ、作成を完了する。
6. 作成したユーザー名の名前をクリックし、「セキュリティ認証情報」タブを開く。
7. 「アクセスキーを作成」をクリックし、ユースケースで「CLI」を選択してキーを作成する。
8. 画面に表示される「アクセスきー」と「シークレットアクセスキー」をコピーして手元に控える。

## AWS CLIのインストール
ターミナルからAWSを直接操作するための公式ツール（AWS CLI）をインストールする。
ターミナルを開き、以下のコマンドを順番に実行する。

```
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

インストールが完了したら、正しく入っているか確認する。

```
aws --version
```

`aws-cli/2.x.x ...`と表示されていれば成功。

## AWSと紐付ける
ターミナルで以下のコマンドを実行する。

```
aws configure
```

実行すると、順番に４つの質問をされるため、以下のように入力していく。

1. `AWS Access Key ID [None]` → アクセスキーを貼り付け
2. `AWS Secret Access Key [None]` → シークレットアクセスキーを貼り付け
3. `Default region name [None]` → ap-northeast-1
4. `Default output format [None]` → json

## コンテナの打ち上げ
### ECRの作成
AWS上に `cosme-app` という名前の専用の倉庫を作成する。
ターミナルで以下のコマンドを実行する。

```
aws ecr create-repository --repository-name cosme-app --region ap-northeast-1
```

### DockerにAWSへの許可を与える
ターミナルで以下のコマンドを実行する。

```
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-northeast-1.amazonaws.com
```

`Login Succeeded` と表示されれば成功。

### コンテナに「AWS行きの宛先ラベル」を貼る
手元の `cosme-app` というコンテナに、先ほどの倉庫へ向かうための宛先ラベルを貼り付ける。
ターミナルで以下のコマンドを実行する。

```
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
docker tag cosme-app:latest $ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/cosme-app:latest
```

### AWSの倉庫へアップロード
ターミナルで、以下のコマンドを実行する。

```
docker push $ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/cosme-app:latest
```
**※**URLは後に12桁の数字で打ち込まないといけないため、ここである作業を行なっておく。
1. 検索窓で`ECR`と検索し、「Elastic Container Registry」を開く。
2. リポジトリ一覧にある倉庫をクリックする。
3. 「URIのコピー」を押し、コピーする。（数字のURL）

## Amazone ECSでWebアプリを公開
### クラスターの作成
コンテナを動かすための「グラウンド」を用意する。
1. 検索窓で `ECS` と検索し、「Elastic Container Service」を開く。
2. 左側のメニューバーから「クラアスター」を選び、「クラスターの作成」をクリックする。
3. クラスター名を入力する。
4. インフラストラクチャはデフォルトのAWS Fargateにチェックが入っている事を確認し、「作成」をクリックする。
**※**　本分析に使用したPC環境が最新ではなかったため、「インフラストラクチャの要件」セクションの「タスクサイズ」や「オペレーションシステム/アーキテクチャ」が選べる箇所を探し、アーキテクチャのプルダウンを`ARM64`に変更した。

### タスク定義の作成
「ECRのあるコンテナをどのポートで動かすか」という指示書を作る。
1. 左側のメニューバーから「タスク定義」を選び、「新しいタスク定義の作成」をクリックする。
2. タスク定義ファミリーを入力する。
3. 起動タイプ: AWS Fargateを選択する。
4. CPUとメモリ: 最小構成の `.25 vCPU` と `.5 GB` を選択する。
5. コンテナ-1の設定欄:
   * 名前: 任意。
   * イメージ URI: 先ほどコピーしたECRの数字のURIを貼り付ける。
   * ポートマッピング: コンテナポートを`8501`に変更する。
6. 一番下の「作成」をクリックする。

### タスクの実行とセキュリティ設定
1. 左側のメニューバーから「クラスター」を開き、作成したクラスターを開く。
2. 「タスク」タブを開き、「新しいタスクの実行」をクリックする。
3. コンピューティングオプション：`起動タイプ`を選び、`Fargate`を選択。
4. デプロイ設定: タスク定義のファミリーで、作成したタスクを選択する。
5. ネットワーキング:
   * セキュリティグループ: 「新しいセキュリティグループの作成」を選択。
   * インバウンドルール:
     * タイプ: カスタム TCP
     * ポート範囲: 8501
     * ソース: Anywhere
   * パブリック IP: 「オン」であることを確認。
6. 「タスクの実行」をクリックする。

**※** ここで、「ECR」・「ECS」ともにregionが一致しているかを確認する。

* **アプリの確認方法**:ステータスが `実行中` になったら、その他タスクIDを開き、「設定」または「ネットワーク」項目の「**パブリック IP**」の数字をコピーし、ブラウザのURL欄にペーストしてアクセスする。