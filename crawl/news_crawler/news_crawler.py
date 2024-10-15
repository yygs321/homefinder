import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



# 3개월 전 날짜 계산
today = datetime.today()
three_months_ago = today - timedelta(days=90)


# 네이버 뉴스 크롤링 함수
def crawl_news(city_no, dvsn_no):
    page = 1
    base_url = f"https://m2.land.naver.com/news/region?cityNo={city_no}&dvsnNo={dvsn_no}&page="

    while True:
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        news_list = soup.select('ul#newsList li.u_lst_l')

        if not news_list:
            print(f"더 이상 뉴스가 없습니다. (페이지: {page})")
            break

        for news_item in news_list:
            title = news_item.select_one('strong.tit').text.strip()
            date_str = news_item.select_one('em.if_text').text.strip().split()[-1]  # 날짜 부분만 추출

            # 날짜 파싱
            pub_date = datetime.strptime(date_str, '%Y.%m.%d')

            # 날짜가 3개월 이전이면 크롤링 중단
            if pub_date < three_months_ago:
                print(f"날짜가 3개월 이전입니다. (날짜: {pub_date})")
                return


        print(f"{page} 페이지 크롤링 완료.")
        page += 1  # 다음 페이지로 이동


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
    crawl_news(city_no="1100000000", dvsn_no=dvsn_no)


