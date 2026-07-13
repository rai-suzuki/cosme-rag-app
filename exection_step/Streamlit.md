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

## 3.アプリの起動
`app.py`があるディレクトリに移動し、以下のプロンプトを実行する。
**※** 仮想環境空間で実行する事を強く推奨する。

```
streamlit run app.py
```