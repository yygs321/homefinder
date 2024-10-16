import csv
import os
from django.core.management.base import BaseCommand
from homefind.models import RealEstate

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            type=str,
            help='CSV 파일이 있는 폴더 경로를 지정합니다.',
        )

    def handle(self, *args, **options):
        folder_path = options['folder']  # 명령어에서 받은 폴더 경로
        if not folder_path:
            self.stdout.write(self.style.ERROR('폴더 경로를 지정해 주세요.'))
            return

        # 폴더 경로에 있는 모든 파일을 순회
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):  # CSV 파일만 처리
                file_path = os.path.join(folder_path, filename)
                self.stdout.write(self.style.NOTICE(f'{filename} 파일 처리 중...'))

                # CSV 파일 읽기 및 데이터베이스에 삽입
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        RealEstate.objects.create(
                            region_id=row['region_id'],
                            price=row['price'],
                            rent_price=row['rent_price'],
                            category=row['category'],
                            house_name=row['house_name'],
                            type=row['type']
                        )

                self.stdout.write(self.style.SUCCESS(f'{filename} 파일 데이터베이스 삽입 완료!'))

        self.stdout.write(self.style.SUCCESS('모든 CSV 파일 처리 완료!'))
