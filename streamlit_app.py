import streamlit as st
import requests
import pandas as pd
import re
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
def fetch_real_estate_data(referer):
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

    all_data = []
    for page in range(1, 11):  # 최대 10페이지까지 데이터 가져오기
        url = f'https://new.land.naver.com/api/articles/complex/{complex_no}?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=&page={page}&complexNo={complex_no}'
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

    # 사용자로부터 referer URL 입력받기
    referer = st.text_input("Enter the referer URL:", placeholder="https://new.land.naver.com/complexes/6142?ms=...")

    # 필터링 옵션들
    trade_type = st.selectbox("Select Trade Type", ["전체", "매매", "전세", "월세"])
    급매_check = st.checkbox("급매")
    로얄_check = st.checkbox("로얄")
    min_price_check = st.checkbox("최저가")
    max_price_check = st.checkbox("최고가")

    # 버튼을 클릭하여 데이터 가져오기
    if st.button('Fetch Data'):
        if referer:
            data = fetch_real_estate_data(referer)

            # 필터링 - 사용자가 선택한 옵션에 따라 데이터 필터링
            if data:
                # 거래형태 필터링
                if trade_type != "전체":
                    data = [row for row in data if row[3] == trade_type]

                # 급매 체크박스 필터링
                if 급매_check:
                    data = [row for row in data if row[11] and '급매' in row[11]]

                # 로얄 체크박스 필터링
                if 로얄_check:
                    data = [row for row in data if row[11] and '로얄' in row[11]]

                # 가격 데이터 필터링
                valid_prices = []
                for row in data:
                    try:
                        # 가격 데이터를 정수로 변환
                        price_str = re.sub(r'[^\d]', '', row[6])  # 숫자 이외의 문자 제거
                        price = int(price_str)
                        valid_prices.append((price, row))
                    except (ValueError, AttributeError):
                        continue  # 잘못된 가격 데이터는 건너뜀

                # 최저가/최고가 필터링
                if valid_prices:
                    if min_price_check:
                        min_price = min(valid_prices, key=lambda x: x[0])[0]
                        valid_prices = [entry for entry in valid_prices if entry[0] == min_price]
                    if max_price_check:
                        max_price = max(valid_prices, key=lambda x: x[0])[0]
                        valid_prices = [entry for entry in valid_prices if entry[0] == max_price]

                    # 필터링된 데이터만 가져오기
                    data = [row for _, row in valid_prices]

                # 필터링된 데이터가 있을 경우 보여주기
                if data:
                    df = pd.DataFrame(data, columns=[
                        "확인날짜", "물건명", "물건형태", "거래형태", "물건동수", "층정보", 
                        "호가", "단지내 이름", "공급면적", "전용면적", "방위", "부가정보", "부동산명"
                    ])
                    st.dataframe(df)

                    # 다운로드 버튼
                    excel_file = BytesIO()
                    df.to_excel(excel_file, index=False, engine='openpyxl')
                    excel_file.seek(0)
                    st.download_button(label="Download as Excel", data=excel_file, file_name="real_estate_data.xlsx")
                else:
                    st.warning("No data found for the selected options.")
            else:
                st.warning("No data found.")
        else:
            st.warning("Please enter a referer URL.")

if __name__ == "__main__":
    create_streamlit_app()
