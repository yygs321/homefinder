import json
import os
from django.core.management.base import BaseCommand
from homefind.models import Region  

class Command(BaseCommand):
    help = 'Load region data from JSON file into the database'

    def handle(self, *args, **kwargs):
        # JSON 파일 경로
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
        json_file_path = os.path.join(base_dir, '../../prop_crawler/region_json/region_list_seoul.json')
        # json_file_path = '../../prop_crawler/region_json/region_list_seoul.json'

        # JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        regions = data['result']['list']
        
        for region_data in regions:
            region_id = region_data['CortarNo'][:5]  # CortarNo의 앞 5자리
            region_name = region_data['CortarNm']  # CortarNm
            
            # Region 객체 생성 및 저장
            region_instance = Region(id=region_id, region_name=region_name)
            try:
                region_instance.save()
                print(f"Region {region_name} added with ID {region_id}.")
            except Exception as e:
                print(f"Failed to add region {region_name}: {e}")

