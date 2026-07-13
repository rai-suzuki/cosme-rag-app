import streamlit as st
import pandas as pd
import os
from langchain_community.document_loaders import DataFrameLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. APIキーの設定
os.environ["OPENAI_API_KEY"] = "Your_Key"

# 2. データの読み込みとデータベース構築
@st.cache_resource
def load_knowledge_base():
    df = pd.read_csv("cosmetics.csv")
    df = df.dropna(subset=['Ingredients', 'Name'])
    df['ai_context'] = "ブランド: " + df['Brand'] + "\n商品名: " + df['Name'] + " (" + df['Label'] + ")\n成分: " + df['Ingredients']
    
    loader = DataFrameLoader(df, page_content_column="ai_context")
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

retriever = load_knowledge_base()

# 3. LLMとプロンプトの設定
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_template("""
                                          
あなたは美容・コスメ専門のプロフェッショナルなAIエンジニア兼アドバイザーです。
以下の参考情報（Sephoraのコスメ成分データベース）のみを用いて、ユーザーの質問に答えてください。

<参考情報>
{context}
</参考情報>

ユーザーの質問: {input}
""")

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ==========================================
# 4. StreamlitでのUI（画面）構築
# ==========================================
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