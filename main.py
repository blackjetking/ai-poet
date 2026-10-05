import os

# from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st


# .env 파일 로드
# load_dotenv()

# Gemini API Key 확인
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY 설정되지 않았습니다.")

llm = init_chat_model( model="google_genai:gemini-3.1-flash-lite-preview", temperature=0)

# 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are a helpful assistant."),
        ("user" , "{input}"),
    ]
)

# 문자열 출력 파서 
output_parser = StrOutputParser()

# LLM 체인 구성 
chain = prompt | llm | output_parser

# 제목 
st.title("인공지능 시인")

# 시 주제 입력필드
content = st.text_input("시의 주제를 제시해 주세요")
st.write("시의 주세는", content)

# 시 작성 요청하기
if st.button("시 작성 요청하기"):
    with st.spinner("Loading"):
        result = chain.invoke({"input" : content + "에 대한 시를 작성해줘"})
        st.write(result)