from collections import Counter
from django.db.models import Count, Avg
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MapData(generics.GenericAPIView):
    def get(self, request):
        # Query parameters에서 최소, 최대 가격 및 카테고리 목록 가져오기
        min_big_price = request.query_params.get('min_big_price')
        max_big_price = request.query_params.get('max_big_price')
        min_small_price = request.query_params.get('min_small_price')
        max_small_price = request.query_params.get('max_small_price')
        selected_category = request.query_params.get('category')

        # 필터링 조건에 따라 쿼리셋 만들기
        realests = RealEstate.objects.all()

        # big_price = 매매가, 전세금 등 큰 금액의 필터 기준
        if min_big_price:
            realests = realests.filter(price__gte=min_big_price)

        if max_big_price:
            realests = realests.filter(price__lte=max_big_price)

        # small_price = 월세, 작은 금액의 필터 기준
        if min_small_price:
            realests = realests.filter(rent_price__gte=min_big_price)

        if max_small_price:
            realests = realests.filter(rent_price__lte=max_big_price)

        # 카테고리 = 건물 종류(빌라, 원룸)
        if selected_category:
            category_list = selected_category.split(',')
            realests = realests.filter(category__in=category_list)

        # 자치구별로 카테고리의 평균 가격 계산
        avg_prices = realests.values('region__region_name', 'category').annotate(avg_price=Avg('price'), avg_rent_price=Avg('rent_price'))

        # 결과 형식을 필요한 대로 수정하여 반환
        data = {}
        for item in avg_prices:
            region_name = item['region__region_name']
            category = item['category']
            avg_price = item['avg_price']
            avg_rent_price = item['avg_rent_price']

            if region_name not in data:
                data[region_name] = []

            if category != 'monthlyRent':
                data[region_name].append({
                    'category': category,
                    'avg_price': avg_price
                })
            else:
                data[region_name].append({
                    'category': category,
                    'avg_price': avg_price,
                    'avg_rent_price': avg_rent_price
                })

        return Response(data, status=status.HTTP_200_OK)


class ForSaleCountByGu(generics.GenericAPIView):
    serializer_class = RealEstateSerializer
    
    def get_queryset(self, *args, **kwagrs):
        return RealEstate.objects.values('region__region_name').annotate(count=Count('id'))
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset, status=status.HTTP_200_OK)


class ForSaleCountByType(generics.GenericAPIView):
    serializer_class = RealEstateSerializer
    
    def get_queryset(self, *args, **kwagrs):
        return RealEstate.objects.values('type').annotate(count=Count('id'))
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset, status=status.HTTP_200_OK)


class WordCloudData(generics.GenericAPIView):
    def get(self, request):
        # 매물명, 지명, 표현을 기준으로 빈도수 세기
        realests = RealEstate.objects.all()

        # 매물명 빈도수 세기
        house_names = [r.house_name for r in realests if r.house_name]  # 매물명 가져오기
        name_counts = Counter(house_names)

        # 지명 빈도수 세기
        regions = [r.region.region_name for r in realests]  # 지명 가져오기
        region_counts = Counter(regions)

        # 결과 조합
        words = []
        for word, count in name_counts.items():
            words.append({"word": word, "count": count})
        for word, count in region_counts.items():
            words.append({"word": word, "count": count})

        # 빈도수에 따라 정렬 (가장 많이 나타나는 것부터)
        words.sort(key=lambda x: x['count'], reverse=True)

        return Response({"words": words}, status=status.HTTP_200_OK)


class ForSaleCountByCategory(generics.GenericAPIView):
    def get(self, request):
        # 데이터베이스에서 거래 방식 가져오기
        realests = RealEstate.objects.all()

        # 거래 방식 카운트하기
        categories = [r.category for r in realests]  # 거래 방식 가져오기
        category_counts = Counter(categories)

        # 결과 조합
        category_data = []
        for category, count in category_counts.items():
            category_data.append({"category": category, "count": count})

        return Response({"categories": category_data}, status=status.HTTP_200_OK)


class HeatMapData(generics.GenericAPIView):
    def get(self, request):
        return Response("Will be Implemented")