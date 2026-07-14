# Streamlitでチャットアプリ化

## 1.ツールのインストール
ターミナルで以下のコマンドを実行し、**Streamlit**をインストールする。

```
pip install streamlit
```

## 2.アプリ本体のファイルを作成
チャットボットを作成した内容に、以下のコードを追加して`app.py`ファイルを作成する。

```
# 4. StreamlitでのUI（画面）構築

st.title("AI コスメアドバイザー")
st.write("Sephoraの成分データに基づき、あなたにぴったりのコスメを提案します。")

# ユーザーからの入力を受け付けるチャット入力欄
user_query = st.chat_input("例：乾燥肌におすすめの化粧水を教えて")

if user_query:
    # ユーザーの質問を画面に表示
    with st.chat_message("user"):
        st.write(user_query)
    
    # AIの回答を生成して画面に表示
    with st.chat_message("assistant"):
        with st.spinner("成分データベースを検索中..."):
            response = rag_chain.invoke(user_query)
            st.write(response)
```

### コード解説(Streamlit)

```
user_query = st.chat_input("例：乾燥肌におすすめの化粧水を教えて")
```
* 画面の下部に、LINEやChatGPTのような「チャット入力用のテキストボックス」を配置するコマンド。
* カッコの中の文字列は「プレースホルダー」と呼ばれ、入力前に薄く表示されるヒント文。
* ユーザーが文字を打ち込みEnterキーを押すと、入力内容が`user_query`に代入される。

```
with st.chat_message("user"):
```
* チャットUIにおける「ユーザー側の吹き出し」の枠組みを作成。`with`を使うことで、この後の処理はこのユーザーの吹き出しの中で行われる。

```
with st.spinner("成分データベースを検索中..."):
```
* 処理が終わるまでの間、ローディングアニメーションとメッセージを表示。


## 3.アプリの起動
`app.py`があるディレクトリに移動し、以下のプロンプトを実行する。
**※** 仮想環境空間で実行する事を強く推奨する。

```
streamlit run app.py
```