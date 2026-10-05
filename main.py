import os
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# 모델명을 정식 ID인 "gemini-2.5-flash"로 변경
llm = init_chat_model(
    model="gemini-2.5-flash", 
    model_provider="google_genai",
    temperature=0.7
)

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 감성적이고 뛰어난 문장력을 가진 인공지능 시인입니다."),
        ("user", "{input}"),
    ]
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit UI
st.title("인공지능 시인")

content = st.text_input("시의 주제를 제시해 주세요")

if content:
    st.write("선택한 시의 주제:", content)

if st.button("시 작성 요청하기"):
    if not content.strip():
        st.warning("주제를 입력해 주세요.")
    else:
        with st.spinner("Loading..."):
            try:
                result = chain.invoke({"input": f"'{content}'에 대한 시를 작성해줘"})
                st.write(result)
            except Exception as e:
                st.error(f"오류 발생: {e}")