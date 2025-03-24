import streamlit as st

# 페이지 선택
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["네이버 아파트 분석", "카카오톡 대화 분석"])

if page == "네이버 아파트 분석":
    import naverapt_app  # 네이버 아파트 분석 페이지 로드
elif page == "카카오톡 대화 분석":
    import katalkranking  # 카카오톡 대화 분석 페이지 로드