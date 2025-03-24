import streamlit as st

# 페이지 선택
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["네이버 아파트 분석", "카카오톡 대화 분석"])

if page == "네이버 아파트 분석":
    exec(open("naverapt_app.py", encoding="utf-8").read())  # 스크립트 실행
elif page == "카카오톡 대화 분석":
    exec(open("katalkranking.py", encoding="utf-8").read())  # 스크립트 실행
