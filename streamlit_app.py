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
    for page in range(1, 11):  # fetch up to 10 pages
        url = f'https://new.land.naver.com/api/articles/complex/{complex_no}?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo={complex_no}&buildingNos=&areaNos=&type=list&order=rank'
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
            st.error(f"Failed to fetch data for page {page}")
    return all_data

# Streamlit 앱 생성
def create_streamlit_app():
    st.title('Real Estate Data Fetcher')

    # 사용자로부터 referer URL 입력받기
    referer = st.text_input("Enter the referer URL:", placeholder="https://new.land.naver.com/complexes/6142?ms=...")

    if st.button('Fetch Data'):
        if referer:
            data = fetch_real_estate_data(referer)

            # Display the data in a table using pandas
            if data:
                df = pd.DataFrame(data, columns=[ 
                    "확인날짜", "물건명", "물건형태", "거래형태", "물건동수", "층정보", 
                    "호가", "단지내 이름", "공급면적", "전용면적", "방위", "부가정보", "부동산명"
                ])
                st.dataframe(df)

                # Allow the user to download the data as an Excel file
                # Create a BytesIO object to store the Excel file in memory
                excel_file = BytesIO()
                df.to_excel(excel_file, index=False, engine='openpyxl')
                excel_file.seek(0)  # Go back to the beginning of the file

                # Provide the download button
                st.download_button(label="Download as Excel", data=excel_file, file_name="real_estate_data.xlsx")

            else:
                st.warning("No data found.")
        else:
            st.warning("Please enter a referer URL.")

if __name__ == "__main__":
    create_streamlit_app()
