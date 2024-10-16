import os
import json
import datetime
import csv
import time
import requests

class PropertyCrawler:
    def __init__(self, folder_path, csv_file_path):
        self.folder_path = folder_path
        self.csv_file_path = csv_file_path
        # FIXME: pyeongsu 삭제 등 데이터 변경 적용
        self.fieldnames = [
            're_id', 'region_id', 'price', 'rent_price', 
            'category', 'pyeongsu', 'house_name', 
            'spec_address', 'type'
        ]

    def crawl_prop_list(self, dong, writer):
        dong_code = dong['CortarNo']
        lon = float(dong['MapXCrdn'])
        lat = float(dong['MapYCrdn'])
        boundaries = self._get_boundaries(lat, lon)

        url = 'https://m.land.naver.com/cluster/ajax/articleList'
        params = self._create_params(dong_code, lat, lon, boundaries)
        headers = self._create_headers()

        data_len = 20
        while data_len >= 20:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)

            # 응답 JSON 데이터 파싱
            data = response.json()
            body_data = data.get('body', [])
            data_len = len(body_data)

            # 데이터 작성
            self._write_data(body_data, writer)

    def _get_boundaries(self, lat, lon):
        # 상하 위도 차이
        lat_diff = 0.02537
        # 좌우 경도 차이
        lon_diff = 0.0216722
        
        # 계산된 경계 값
        top = lat + lat_diff
        btm = lat - lat_diff
        rgt = lon + lon_diff
        lft = lon - lon_diff
        
        return {
            'top': top,
            'btm': btm,
            'rgt': rgt,
            'lft': lft
        }
    
    def _create_params(self, dong_code, lat, lon, boundaries):
        return {
            'rletTpCd': 'OPST:VL:OR',
            'tradTpCd': 'A1:B1:B2',
            'z': 14,
            'lat': lat,
            'lon': lon,
            'btm': boundaries['btm'],
            'lft': boundaries['lft'],
            'top': boundaries['top'],
            'rgt': boundaries['rgt'],
            'spcMax': 33,
            'rprcMax': 50,
            'showR0': '',
            'cortarNo': dong_code,
            'page': 0,
        }

    def _create_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }

    def _write_data(self, body_data, writer):
        for item in body_data:
            time.sleep(0.5)
            # FIXME: 여기도 데이터 변경 적용
            writer.writerow({
                're_id': item.get('atclNo'),
                'region_id': item.get('cortarNo'),
                'price': item.get('prc'),
                'rent_price': item.get('rentPrc'),
                'category': item.get('tradTpNm'),
                'pyeongsu': item.get('spc1'),
                'house_name': item.get('atclNm'),
                'spec_address': '',
                'type': item.get('rletTpNm'),
            })

    def start_crawling(self):
        with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()

            for filename in os.listdir(self.folder_path):
                if filename.endswith('00000.json'):
                    file_path = os.path.join(self.folder_path, filename)
                    self._process_json_file(file_path, writer)

    def _process_json_file(self, file_path, writer):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
                dong_data = data['result']['list']
                # FIXME: print 삭제
                print(data['result']['dvsnInfo']['CortarNm'], '-------------------')
                for dong in dong_data:
                    print(f"{dong['CortarNm']} 시작")
                    self.crawl_prop_list(dong, writer)
                    print(f"{dong['CortarNm']} 완료")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")


if __name__ == "__main__":
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    csv_file_path = f'property_data/crawled_{today}.csv'
    print(csv_file_path)

    folder_path = './region_json'
    crawler = PropertyCrawler(folder_path, csv_file_path)
    crawler.start_crawling()
    print(f'Data with atclNo and cortarNo has been written to {csv_file_path}.')
