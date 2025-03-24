import streamlit as st
import pandas as pd
from collections import defaultdict
import re
from io import StringIO

# 카카오톡 대화 텍스트 파일 파싱 함수
def parse_kakao_chat(file):
    lines = file.getvalue().decode("utf-8").splitlines()
    date_pattern = re.compile(r'^-+ (\d{4}년 \d{1,2}월 \d{1,2}일 [가-힣]+) -+$')
    message_pattern = re.compile(r'^\[(.*?)\] \[(.*?)\] (.*)$')
    
    messages = []
    current_date = None
    
    for line in lines:
        # 날짜 줄인지 확인
        date_match = date_pattern.match(line)
        if date_match:
            current_date = date_match.group(1)  # 날짜 추출
            continue
        
        # 메시지 줄인지 확인
        message_match = message_pattern.match(line)
        if message_match and current_date:
            nickname = message_match.group(1).strip()  # 닉네임의 공백 제거
            message = message_match.group(3)
            messages.append((current_date, nickname, message))
    
    return messages

# 주요 메시지 추출 함수
def extract_key_messages(messages, min_length=20, keywords=None):
    if keywords is None:
        keywords = ["회의", "약속", "중요", "필수", "확인", "요청"]  # 기본 키워드 설정
    
    key_messages = []
    for msg in messages:
        # 긴 메시지 또는 키워드가 포함된 메시지를 주요 메시지로 선택
        if len(msg[2]) >= min_length or any(keyword in msg[2] for keyword in keywords):
            key_messages.append(msg)
    return key_messages

# 링크 추출 함수
def extract_links(text):
    # 정규식을 사용하여 URL 추출
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.findall(text)

# Streamlit 앱
def main():
    st.title("카카오톡 대화 분석기")

    # 파일 업로드
    uploaded_file = st.file_uploader("카카오톡 대화 텍스트 파일을 업로드하세요.", type=["txt"])

    if uploaded_file is not None:
        # 파일 파싱
        messages = parse_kakao_chat(uploaded_file)
        
        # 날짜 추출 및 중복 제거
        dates = sorted(list(set([msg[0] for msg in messages])))
        
        # 드롭다운 리스트 박스로 날짜 선택
        selected_date = st.selectbox("날짜를 선택하세요.", dates)
        
        # 선택된 날짜에 해당하는 메시지 필터링
        filtered_messages = [msg for msg in messages if msg[0] == selected_date]
        
        # 닉네임별 메시지 개수 계산
        message_count = defaultdict(int)
        for msg in filtered_messages:
            message_count[msg[1]] += 1
        
        # 비율 계산
        total_messages = len(filtered_messages)
        nickname_stats = []
        for nickname, count in message_count.items():
            ratio = (count / total_messages) * 100
            nickname_stats.append((nickname, count, ratio))
        
        # DataFrame 생성
        df = pd.DataFrame(nickname_stats, columns=["닉네임", "메시지 개수", "비율 (%)"])
        
        # 동률 처리 (메시지 개수 기준으로 순위 부여)
        df["순위"] = df["메시지 개수"].rank(method="min", ascending=False).astype(int)
        
        # 탑텐 정렬
        top_10 = df.sort_values(by="순위").head(10)
        
        # 결과 표시 (인덱스 숨기기)
        st.write(f"선택된 날짜: {selected_date}")
        st.table(top_10[["순위", "닉네임", "메시지 개수", "비율 (%)"]].set_index("순위"))
        
        # 특정 닉네임 필터링 (닉네임에 '스탭'이 포함된 경우)
        target_messages = [msg for msg in filtered_messages if "스탭" in msg[1]]
        
        # 링크 추출 및 정리
        target_messages_with_links = []
        for msg in target_messages:
            links = extract_links(msg[2])
            if links:
                for link in links:
                    # 링크를 하이퍼링크로 변환
                    hyperlink = f'<a href="{link}" target="_blank">{link}</a>'
                    target_messages_with_links.append((msg[0], msg[1], msg[2], hyperlink))
            else:
                # 링크가 없는 경우
                target_messages_with_links.append((msg[0], msg[1], msg[2], "링크 없음"))
        
        # 특정 닉네임의 메시지와 링크를 DataFrame으로 변환
        target_messages_df = pd.DataFrame(target_messages_with_links, columns=["날짜", "닉네임", "메시지", "링크"])
        
        # 닉네임을 가로로 표시하기 위해 그룹화
        grouped_messages = target_messages_df.groupby("닉네임").agg({
            "메시지": lambda x: "<br>".join(x),  # 메시지를 <br> 태그로 구분하여 가로로 나열
            "링크": lambda x: "<br>".join(x)     # 링크를 <br> 태그로 구분하여 가로로 나열
        }).reset_index()
        
        # 특정 닉네임의 메시지와 링크 표시 (하이퍼링크 적용)
        st.write("특정 닉네임의 메시지 및 링크 (닉네임에 '스탭'이 포함된 경우):")
        st.write(
            grouped_messages.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
        
        # 탑 10 닉네임 추출
        top_10_nicknames = top_10["닉네임"].tolist()
        
        # 탑 10 닉네임에 해당하는 메시지 추출
        top_10_messages = [msg for msg in filtered_messages if msg[1] in top_10_nicknames]
        
        # 주요 메시지 추출
        key_messages = extract_key_messages(top_10_messages, min_length=20)
        
        # 주요 메시지를 DataFrame으로 변환
        key_messages_df = pd.DataFrame(key_messages, columns=["날짜", "닉네임", "주요 메시지"])
        
        # 주요 메시지 표시
        st.write("탑 10 닉네임의 주요 메시지:")
        st.table(key_messages_df[["닉네임", "주요 메시지"]])

if __name__ == "__main__":
    main()