from django.db.models import Count

from crawl.news_crawler.news_crawler import check_cache_and_collect_data
from crawl.wordcloud.wordcloud_generator import generate_wordcloud
from .models import *
from .serializers import *
from django.shortcuts import render
from django.db.models import Avg


def index(request):
    districtData1 = {}  # 매매, 전세, 월세를 선택하면 빌라 - 오피스텔 - 원룸 순서로 매물량 막대그래프
    districtData2 = {}  # 빌 - 오 - 원 선택하면 매매 - 전세 - 월세 순서로 매물량 막대 그래프
    donutDistrictData1 = {}  # 월세 - 전세 - 매매 순서 파이차트
    donutDistrictData2 = {}  # 빌 - 오 - 원 파이차트

    regions = Region.objects.all()

    for region in regions:
        districtData1[region.region_name] = {'sales': [0] * 3, 'rent': [0] * 3, 'monthly': [0] * 3}
        districtData2[region.region_name] = {'villa': [0] * 3, 'officetel': [0] * 3, 'oneroom': [0] * 3}
        donutDistrictData1[region.region_name] = [0] * 3
        donutDistrictData2[region.region_name] = [0] * 3

    realests = RealEstate.objects.all()

    # 1. districtData1 완성
    for r in regions:
        gu = r.region_name
        gu_reals = realests.filter(region__region_name=gu)

        # 카테고리(매매,전세,월세) / type(빌 - 오 - 원)으로 groupby 후 count
        translation = {'매매': 'sales', '전세': 'rent', '월세': 'monthly'}
        orders = {'빌라': 0, '오피스텔': 1, '원룸': 2}
        for counting in gu_reals.values('category', 'type').annotate(count=Count('id')):
            districtData1[gu][translation[counting['category']]][orders[counting['type']]] = counting['count']

    # 2. districtData2 완성
    for r in regions:
        gu = r.region_name
        gu_reals = realests.filter(region__region_name=gu)

        # type(빌 - 오 - 원) / 카테고리(매매,전세,월세)으로 groupby 후 count
        translation = {'빌라': 'villa', '오피스텔': 'officetel', '원룸': 'oneroom'}
        orders = {'매매': 0, '전세': 1, '월세': 2}
        for counting in gu_reals.values('type', 'category').annotate(count=Count('id')):
            districtData2[gu][translation[counting['type']]][orders[counting['category']]] = counting['count']

    # 3. donutDistrictData1 완성
    for r in regions:
        gu = r.region_name
        gu_reals = realests.filter(region__region_name=gu)

        # 카테고리(매매,전세,월세)으로 groupby 후 count
        orders = {'월세': 0, '전세': 1, '매매': 2}
        for counting in gu_reals.values('category').annotate(count=Count('id')):
            donutDistrictData1[gu][orders[counting['category']]] = counting['count']

    # 4. donutDistrictData2 완성
    for r in regions:
        gu = r.region_name
        gu_reals = realests.filter(region__region_name=gu)

        # type(빌라, 오피스텔, 원룸)으로 groupby 후 count
        orders = {'빌라': 0, '오피스텔': 1, '원룸': 2}
        for counting in gu_reals.values('type').annotate(count=Count('id')):
            donutDistrictData2[gu][orders[counting['type']]] = counting['count']

    context = {
        "districtData1": districtData1,
        "districtData2": districtData2,
        "donutDistrictData1": donutDistrictData1,
        "donutDistrictData2": donutDistrictData2,
    }

    return render(request, "index.html", context=context)

def map(request):
    # Initialize an empty dictionary to store the data
    region_data = {}

    # Mapping building_type values to dictionary keys
    building_type_map = {
        '빌라': 'villa',
        '오피스텔': 'officetel',
        '원룸': 'oneroom'
    }

    # Get all regions
    regions = Region.objects.all()

    # Iterate over each region
    for region in regions:
        # Initialize the structure for each region
        region_data[region.region_name] = {
            'villa': {'매매': 0, '전세': 0, '월세': {'보증금': 0, '월세': 0}},
            'officetel': {'매매': 0, '전세': 0, '월세': {'보증금': 0, '월세': 0}},
            'oneroom': {'매매': 0, '전세': 0, '월세': {'보증금': 0, '월세': 0}}
        }

        # Query the average prices for each type and category in this region
        for building_type, mapped_type in building_type_map.items():
            for category in ['매매', '전세', '월세']:
                if category == '월세':
                    # Query for rent_price and price for 월세 category
                    avg_deposit = RealEstate.objects.filter(
                        region=region,
                        type=building_type,
                        category=category
                    ).aggregate(Avg('price'))['price__avg']

                    avg_rent = RealEstate.objects.filter(
                        region=region,
                        type=building_type,
                        category=category
                    ).aggregate(Avg('rent_price'))['rent_price__avg']

                    # If values are not None, store them, else keep 0
                    if avg_deposit is not None:
                        region_data[region.region_name][mapped_type]['월세']['보증금'] = round(avg_deposit, 2)

                    if avg_rent is not None:
                        region_data[region.region_name][mapped_type]['월세']['월세'] = round(avg_rent, 2)

                else:
                    # For 매매 and 전세, calculate price as usual
                    avg_price = RealEstate.objects.filter(
                        region=region,
                        type=building_type,
                        category=category
                    ).aggregate(Avg('price'))['price__avg']

                    if avg_price is not None:
                        # Apply rounding to the average price
                        region_data[region.region_name][mapped_type][category] = round(avg_price, 2)

    # Pass the data to the template
    context = {
        'region_data': region_data
    }

    return render(request, "map.html", context)


def home(request):
    # 첫 번째 페이지: 매물수 비교 막대 차트 위한 데이터 생성
    regions = ['강남구', '서초구', '송파구', '강동구', '마포구', '중구', '종로구', '동대문구', '강북구', '성북구', '노원구', '도봉구', '은평구', '서대문구', '양천구',
               '영등포구', '관악구', '동작구', '광진구', '구로구']
    num_res = [0] * len(regions)

    res = RealEstate.objects.all()

    for i in range(len(regions)):
        r = regions[i]
        num_res[i] = res.filter(region__region_name=r).count()

    context=dict()

    # 두 번째 페이지: 매매, 전세, 월세에 따른 최저가 정보 반환
    context['villas_sale'] = get_top3_res('빌라', '매매')
    context['villas_jeonse'] = get_top3_res('빌라', '전세')
    context['villas_rent'] = get_top3_res('빌라', '월세')

    context['offices_sale'] = get_top3_res('오피스텔', '매매')
    context['offices_jeonse'] = get_top3_res('오피스텔', '전세')
    context['offices_rent'] = get_top3_res('오피스텔', '월세')

    context['ones_sale'] = get_top3_res('원룸', '매매')
    context['ones_jeonse'] = get_top3_res('원룸', '전세')
    context['ones_rent'] = get_top3_res('원룸', '월세')

    context["regions"]=regions
    context["num_res"] = num_res

    # 워드클라우드 이미지 생성
    frequency_data = check_cache_and_collect_data()
    if not frequency_data:
        context['image_url'] = "데이터가 없습니다."
    else:
        # 워드클라우드 이미지 생성
        image_url =generate_wordcloud(frequency_data)
        context['image_url'] = image_url

    return render(request, "main.html", context=context)


def get_top3_res(building_type, transaction_type):
    res = RealEstate.objects.filter(type=building_type, category=transaction_type).order_by('price')[:3]
    result_list = []
    for i, estate in enumerate(res):
        result = f"{i + 1}. {estate.region.region_name} / "
        if estate.category == '월세':
            result += f"월세: {int(estate.rent_price)}만"
        else:
            result += f"{estate.category}: {int(estate.price)}만"
        result_list.append(result)
    return result_list
