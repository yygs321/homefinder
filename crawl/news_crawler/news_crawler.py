from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from crawl.news_crawler.db_connector import check_cache_and_update_if_needed, save_to_db, save_to_redis, get_cached_data
from crawl.news_crawler.frequency_counter import count_frequency
from datetime import datetime,timedelta

# Chrome 드라이버 경로 설정
chrome_service = Service(r'C:\Program Files\chromeDriver\chromedriver-win64\chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

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

def crawl_news(city_no, dvsn_no,frequency_data):
    today = datetime.today()
    six_months_ago = today - timedelta(days=180)
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

            # 빈도수 계산하고 결과를 리스트에 추가
            count_frequency(title, frequency_data, today)

        page += 1

    return

def check_cache_and_collect_data():
    frequency_data = []

    # 캐시를 확인하고 크롤링이 필요한 경우에만 수행
    if check_cache_and_update_if_needed():
        for district, dvsn_no in districts.items():
            print(f'{district} 크롤링 시작')
            crawl_news("1100000000", dvsn_no, frequency_data)
            print(f'{district} 크롤링 종료')
            print("---------------------")

        # DB와 Redis에 저장
        save_to_db(frequency_data)
        save_to_redis(frequency_data)

    else:# 캐시에서 데이터를 가져오거나 크롤링 결과 사용
        frequency_data = get_cached_data()

    return frequency_data