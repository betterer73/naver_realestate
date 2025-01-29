import streamlit as st
import requests
import pandas as pd
import re
import webbrowser
from io import BytesIO

# 쿠키와 헤더 설정
cookies = {
    'NAC': 'AW26BcgB9ClN',
    'NNB': 'FSL5HINTPJPGO',
    '_fwb': '807DNxPwbc442OLiYNhhAb.1734426107631',
    'landHomeFlashUseYn': 'Y',
    '_fwb': '807DNxPwbc442OLiYNhhAb.1734426107631',
    'NID_AUT': 'AVlS2ypK1eKJXaMk/t8ify58fz6CpAlbxJpgJJcBim0DpT1FvDhtihIE4Ouo7hFK',
    'NID_JKL': 'u5YTgXMnsugLxxdU1x6tkqhkGxEahONN1t8/zzRNurs=',
    '_ga': 'GA1.1.1504936074.1735461353',
    '_ga_8P4PY65YZ2': 'GS1.1.1735461353.1.1.1735461354.59.0.0',
    '_ga_451MFZ9CFM': 'GS1.1.1735696153.1.1.1735696156.0.0.0',
    'ASID': '77cbe4fd000001942bde861e0000005b',
    'nstore_session': 'qsJ1mffeKePqkXeoFKtxJXno',
    'nstore_pagesession': 'i3WW3sqlv5FAZssL3rl-092158',
    'page_uid': 'iG3SRsqo1awsskr3sohsssssszZ-044744',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '3000000000',
    'NACT': '1',
    'NID_SES': 'AAABtJgYPEJTG3lJz240w2rBOP+t0HYZz3GAdFAslZuTKiyKiQinkfrUy8U/3DWqQ5r81K2Kp16KR5G8lOhZQFn0qtS1vWKr75RaGvfyF0Bq+rL09QFXUk1GEhB3fmpTJfpBMma/EMOkyIDRDEg42HBEhvPOc+2FEc+kMgJztpeUUk+HfIguSwRmPts/eHQVNLle05EPGnhvrV/hNz7k73guBrLBswiJGwxIhYv7EDu3CAJkwAMvsM0KbJVeCgW6YyWoB84FVu0CUfXf+ZbzsvyM1FkvwyG/eV5gGiUt3Y+NUbqUO61Evfo/M0J/JlRfQmGestWCZi6aS9jN1E8lCsHCI4NRAvaR6UW8hXlojyMA1zYwHC0tA9t5sqD0sXi9Je8FMKtcli0YDf/QihKQWvuzQqqoklxc1gjVeRydTwGJ5PbCBWb0hvW6Y8hahDRi8cFHEOVuNIRWygcxnyY09UCmdy+HKbT7fFB8mnXhW8ZOC/4hH52rCINGopMfy/O2mk6MzFd9secBNsAZ6L0NQiKZKQ+zaHQVwJkCXjPWAchxK/miFTP1Fzwxo6wX7Jq+cI6ez2wYXUytHkdnLXDa7m4YtEM=',
    'SRT30': '1737592628',
    'REALESTATE': 'Thu%20Jan%2023%202025%2009%3A52%3A00%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'BUC': 'ywUbf_THLoowbQDe_KDJzMOJYKX8RIccz3n4TE-tevw=',
}

# API 호출 및 데이터 가져오기 함수
def fetch_real_estate_data(referer, trade_type):
    # Referer에서 complexNo 추출
    match = re.search(r'complexes/(\d+)', referer)
    if not match:
        st.error("Invalid referer URL. Please provide a valid URL containing 'complexes/{complexNo}'.")
        return []

    complex_no = match.group(1)
    headers = {
        'accept': '*/*',
        'accept-language': 'ko',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3Mzc1OTM1MjAsImV4cCI6MTczNzYwNDMyMH0.lv36Tus22GS__NC2e-zKsZ_tmy2nr0jlgaFmM5GfLa0',
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    # trade_type을 API 요청에 맞게 변환
    trade_type_mapping = {
        "전체": "",
        "매매": "A1",  # 매매에 해당하는 API 값
        "전세": "B1",  # 전세에 해당하는 API 값
        "월세": "B2",  # 월세에 해당하는 API 값
    }
    trade_type_param = trade_type_mapping.get(trade_type, "")

    all_data = []
    for page in range(1, 11):  # 최대 10페이지까지 데이터 가져오기
        url = f'https://new.land.naver.com/api/articles/complex/{complex_no}?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType={trade_type_param}&page={page}&complexNo={complex_no}'
        response = requests.get(url, cookies=cookies, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for article in data.get('articleList', []):
                all_data.append([
                    article.get("articleConfirmYmd"),
                    article.get("articleName"),
                    article.get("realEstateTypeName"),
                    article.get("tradeTypeName"),
                    article.get("buildingName"),
                    article.get("floorInfo"),
                    article.get("dealOrWarrantPrc"),
                    article.get("areaName"),
                    article.get("area1"),
                    article.get("area2"),
                    article.get("direction"),
                    article.get("articleFeatureDesc"),
                    article.get("realtorName")
                ])
        else:
            st.error(f"Failed to fetch data for page {page} with status code {response.status_code}")
    return all_data

# Streamlit 앱 생성
def create_streamlit_app():
    st.title('Real Estate Data Fetcher')

    # 1. Enter the referer URL
    referer = st.text_input("Enter the Naver Realestate referer URL:", placeholder="https://new.land.naver.com/complexes/6142?ms=...")

    # 2. Select Trade Type 드롭다운
    trade_type = st.selectbox("Select Trade Type", ["전체", "매매", "전세", "월세"])

    # 3. Fetch Data 버튼
    if st.button('Fetch Data'):
        if referer:
            # API 호출 및 데이터 가져오기
            data = fetch_real_estate_data(referer, trade_type)

            if data:
                df = pd.DataFrame(data, columns=[
                    "확인날짜", "물건명", "물건형태", "거래형태", "물건동수", "층정보", 
                    "호가", "단지내 면적", "공급면적", "전용면적", "방위", "부가정보", "부동산명"
                ])

                # 데이터를 세션 상태에 저장
                st.session_state['df'] = df

                # 초기 결과 표시
                st.dataframe(df)

                # 다운로드 버튼
                excel_file = BytesIO()
                df.to_excel(excel_file, index=False, engine='openpyxl')
                excel_file.seek(0)
                st.download_button(label="Download as Excel", data=excel_file, file_name="real_estate_data.xlsx")
            else:
                st.warning("No data found.")
        else:
            st.warning("Please enter a referer URL.")

    # 4. Select Building Name 드롭다운 (Fetch Data 이후에만 표시)
    if 'df' in st.session_state:
        building_size = st.session_state['df']['단지내 면적'].unique()
        selected_building = st.selectbox("Select Building Size", building_size)

    # 5. 체크박스 필터링 옵션
    급매_check = st.checkbox("급매")
    로얄_check = st.checkbox("로얄")
    min_price_check = st.checkbox("최저가")
    max_price_check = st.checkbox("최고가")

    # 6. 실행 버튼
    if st.button('Run'):
        # 필터링 적용
        filtered_data = st.session_state['df'][st.session_state['df']['단지내 면적'] == selected_building]

        # 급매 체크박스 필터링
        if 급매_check:
                filtered_data = filtered_data[filtered_data['부가정보'].str.contains('급매', na=False)]

        # 로얄 체크박스 필터링
        if 로얄_check:
            filtered_data = filtered_data[filtered_data['부가정보'].str.contains('로얄', na=False)]

        # 가격 데이터 필터링
        if min_price_check or max_price_check:

            # 가격 데이터를 정수로 변환
            filtered_data['호가'] = filtered_data['호가'].str.replace(r'[^\d]', '', regex=True).astype(float)

        if min_price_check:
            min_price = filtered_data['호가'].min()
            filtered_data = filtered_data[filtered_data['호가'] == min_price]

        if max_price_check:
            max_price = filtered_data['호가'].max()
            filtered_data = filtered_data[filtered_data['호가'] == max_price]

        # 필터링된 데이터 표시
        if not filtered_data.empty:
            st.dataframe(filtered_data)

            # 다운로드 버튼
            excel_file = BytesIO()
            filtered_data.to_excel(excel_file, index=False, engine='openpyxl')
            excel_file.seek(0)
            st.download_button(label="Download Filtered Data as Excel", data=excel_file, file_name="filtered_real_estate_data.xlsx")
        else:
            st.warning("No data found for the selected options.")


    # 리치고 열기
    # if st.button("Open the Richgo in Chrome"):
    #    webbrowser.open(f'https://m.richgo.ai/pc')
    st.markdown("[Open the Richgo in Chrome](https://m.richgo.ai/pc)", unsafe_allow_html=True)


if __name__ == "__main__":
    create_streamlit_app()
