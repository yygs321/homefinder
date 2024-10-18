import csv
import os
from django.core.management.base import BaseCommand
from homefind.models import RealEstate, Region

class Command(BaseCommand):
    help = '지정된 폴더 내의 모든 CSV 파일을 읽어서 데이터베이스에 삽입합니다.'

    folder_path = 'crawl/prop_crawler/property_data/'

    def handle(self, *args, **kwargs):
        if not os.path.exists(self.folder_path):
            self.stdout.write(self.style.ERROR(f'{self.folder_path} 경로가 존재하지 않습니다.'))
            return

        # 폴더 경로에 있는 모든 파일을 순회
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.csv'):  # CSV 파일만 처리
                file_path = os.path.join(self.folder_path, filename)
                self.stdout.write(self.style.NOTICE(f'{filename} 파일 처리 중...'))

                # CSV 파일 읽기 및 데이터베이스에 삽입
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        RealEstate.objects.create(
                            region=Region.objects.get(pk=row['region_id']),
                            price=row['price'],
                            rent_price=row['rent_price'],
                            category=row['category'],
                            house_name=row['house_name'],
                            type=row['type']
                        )

                self.stdout.write(self.style.SUCCESS(f'{filename} 파일 데이터베이스 삽입 완료!'))

        self.stdout.write(self.style.SUCCESS('모든 CSV 파일 처리 완료!'))
