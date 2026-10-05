
import os

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ============================================================
# 1. Streamlit Secrets에서 Gemini API Key 가져오기
# ============================================================

api_key = None

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

elif "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]



st.write("GOOGLE_API_KEY 존재:", "GOOGLE_API_KEY" in st.secrets)

# ============================================================
# 2. API Key 확인
# ============================================================

st.title("인공지능 시인")

if not api_key:
    st.error(
        "Gemini API Key가 설정되지 않았습니다.\n\n"
        "Streamlit Cloud → Settings → Secrets에서 "
        "GOOGLE_API_KEY를 설정해주세요."
    )
    st.stop()


# ============================================================
# 3. API Key를 환경변수에 설정
# ============================================================

os.environ["GOOGLE_API_KEY"] = api_key


# ============================================================
# 4. Gemini LLM 초기화
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=api_key,
    temperature=0.7,
)


# ============================================================
# 5. 프롬프트 생성
# ============================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 감성적이고 뛰어난 문장력을 가진 인공지능 시인입니다."
        ),
        (
            "user",
            "{input}"
        ),
    ]
)


# ============================================================
# 6. Output Parser
# ============================================================

output_parser = StrOutputParser()


# ============================================================
# 7. LangChain Chain 구성
# ============================================================

chain = prompt | llm | output_parser


# ============================================================
# 8. 사용자 입력
# ============================================================

content = st.text_input(
    "시의 주제를 제시해 주세요"
)


# ============================================================
# 9. 입력 내용 표시
# ============================================================

if content:
    st.write(f"선택한 시의 주제: **{content}**")


# ============================================================
# 10. 시 작성 버튼
# ============================================================

if st.button("시 작성 요청하기"):

    # 주제 입력 여부 확인
    if not content.strip():
        st.warning("주제를 입력해 주세요.")

    else:

        # Gemini 호출
        with st.spinner("시를 작성하는 중..."):

            try:

                result = chain.invoke(
                    {
                        "input": (
                            f"'{content}'에 대한 시를 작성해줘."
                        )
                    }
                )

                st.write(result)

            except Exception as e:

                st.error(f"Gemini API 호출 중 오류가 발생했습니다.")

                st.exception(e)
