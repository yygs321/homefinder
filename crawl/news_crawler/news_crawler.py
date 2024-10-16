from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from frequency_counter import count_frequency  # 빈도수 계산 함수 import
#from db_connector import save_to_db  # DB 저장 함수 import
import time

# Chrome 드라이버 경로 설정
chrome_service = Service(r'C:\Program Files\chromeDriver\chromedriver-win64\chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

today = datetime.today()
six_months_ago = today - timedelta(days=180)

# 각 자치구별로 빈도수 리스트
frequency_data = []

def crawl_news(city_no, dvsn_no):
    page = 1
    base_url = f"https://m2.land.naver.com/news/region?cityNo={city_no}&dvsnNo={dvsn_no}"

    flag = 0
    while not flag:
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}&page={page}"

        driver.get(url)


        news_list = driver.find_elements(By.CSS_SELECTOR, 'ul#newsList li.u_lst_l')

        if not news_list:
            break

        for news_item in news_list:
            title = news_item.find_element(By.CSS_SELECTOR, 'strong.tit').text.strip()
            date_str = news_item.find_element(By.CSS_SELECTOR, 'em.if_text').text[-11:].split(' ')[-1].replace('.', '')


            pub_date = datetime.strptime(date_str, '%Y%m%d')

            # 날짜가 3개월 이전이면 크롤링 중단
            if pub_date < six_months_ago:
                flag=1
                break

            # 빈도수 계산하고 결과를 DB에 저장
            count_frequency(title, frequency_data, today)
            #save_to_db(frequency_data)

        print(f"{page} 페이지 크롤링 완료.")
        page += 1

    for data in frequency_data:
        print(data)
    return

# 자치구 코드를 사용한 크롤링 실행
districts = {
    "강남구": "1168000000",
    "강동구": "1174000000",
    "강북구": "1130500000",
    "강서구": "1150000000",
    "관악구": "1162000000",
    "광진구": "1121500000",
    "구로구": "1153000000",
    "금천구": "1154500000",
    "노원구": "1135000000",
    "도봉구": "1132000000",
    "동대문구": "1123000000",
    "동작구": "1159000000",
    "마포구": "1144000000",
    "서대문구": "1141000000",
    "서초구": "1165000000",
    "성동구": "1120000000",
    "성북구": "1129000000",
    "송파구": "1171000000",
    "양천구": "1147000000",
    "영등포구": "1156000000",
    "용산구": "1117000000",
    "은평구": "1138000000",
    "종로구": "1111000000",
    "중구": "1114000000",
    "중랑구": "1126000000"
}

# 각 자치구에 대해 크롤링
for district, dvsn_no in districts.items():
    print(f"{district} ({dvsn_no}) 뉴스 크롤링 시작.")
    crawl_news("1100000000", dvsn_no)
    print("----")


