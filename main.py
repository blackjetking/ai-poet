import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Streamlit Secrets에서 API Key 가져와 환경변수로 설정
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# 2. LLM 직접 초기화 (api_key 명시 전달)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",  # 또는 "gemini-1.5-pro"
    google_api_key=api_key,
    temperature=0.7
)

# 3. 프롬프트 및 체인
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 감성적이고 뛰어난 문장력을 가진 인공지능 시인입니다."),
        ("user", "{input}"),
    ]
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# UI 구성
st.title("인공지능 시인")

content = st.text_input("시의 주제를 제시해 주세요")

if content:
    st.write(f"선택한 시의 주제: **{content}**")

if st.button("시 작성 요청하기"):
    if not content.strip():
        st.warning("주제를 입력해 주세요.")
    elif not api_key:
        st.error("Streamlit Secrets에 GOOGLE_API_KEY가 설정되지 않았습니다.")
    else:
        with st.spinner("시를 작성하는 중..."):
            try:
                result = chain.invoke({"input": f"'{content}'에 대한 시를 작성해줘"})
                st.write(result)
            except Exception as e:
                st.error(f"오류 발생: {e}")