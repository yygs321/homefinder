import json
import requests

'''region_list_seoul.json은 서울의 구 데이터를 가지고 있다
이 파일을 이용해서 각 구의 동 데이터를 파일로 저장
구별 파일 생성을 위한 1회성 용도
'''
# region_list_seoul.json 파일을 읽어옵니다.
with open('region_list_seoul.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 요청에 필요한 헤더 설정 (User-Agent 추가)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}

# list에서 각 CortarNo에 대해 URL을 생성하고 요청.
for item in data['result']['list']:
    cortar_no = item['CortarNo']
    
    # URL
    url = f"https://m.land.naver.com/map/getRegionList?cortarNo={cortar_no}&mycortarNo={cortar_no}"
    
    # 요청 보내기
    response = requests.get(url, headers=headers)
    
    # 응답을 CortarNo.json 파일로 저장
    if response.status_code == 200:
        with open(f'{cortar_no}.json', 'w', encoding='utf-8') as outfile:
            json.dump(response.json(), outfile, ensure_ascii=False, indent=4)
        print(f'{cortar_no}.json 파일이 성공적으로 저장되었습니다.')
    else:
        print(f'{cortar_no}에 대한 요청 실패. 상태 코드: {response.status_code}')
