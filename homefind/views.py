from django.db.models import Count
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
            'villa': {'매매': 0, '전세': 0, '월세': 0},
            'officetel': {'매매': 0, '전세': 0, '월세': 0},
            'oneroom': {'매매': 0, '전세': 0, '월세': 0}
        }

        # Query the average prices for each type and category in this region
        for building_type, mapped_type in building_type_map.items():
            for category in ['매매', '전세', '월세']:
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
    # 1페이지 막대 그래프 위한 regions, num_res 배열 만들어 반환
    regions = ['강남구', '서초구', '송파구', '강동구', '마포구', '중구', '종로구', '동대문구', '강북구', '성북구', '노원구', '도봉구', '은평구', '서대문구', '양천구', '영등포구', '관악구', '동작구', '광진구', '구로구']
    num_res = [0] * len(regions)

    res = RealEstate.objects.all()

    for i in range(len(regions)):
        r = regions[i]
        num_res[i] = res.filter(region__region_name=r).count()
    
    context = {
        'regions': regions,
        'num_res': num_res,
    }

    # 2페이지 - 빌라, 오피스텔, 원룸 별 저렴한 건물 보여주기 위한 데이터 반환
    villas = res.filter(type='빌라').order_by('-price')[:3]
    offices = res.filter(type='오피스텔').order_by('-price')[:3]
    ones = res.filter(type='원룸').order_by('-price')[:3]

    context['villas'] = []

    for i in range(len(villas)):
        villa = villas[i]
        result = str(i + 1) + '. ' + str(villa.region.region_name) + '/' 

        if villa.category == '월세':
            result += '월세: ' + str(int(villa.rent_price) // 10000) + '만'
        else:
            result += str(villa.category) + ': ' + str(int(villa.price) // 10000) + '만'
        
        context['villas'].append(result)
    
    context['offices'] = []

    for i in range(len(offices)):
        office = offices[i]
        result = str(i + 1) + '. ' + str(office.region.region_name) + '/' 

        if office.category == '월세':
            result += '월세: ' + str(int(office.rent_price) // 10000) + '만'
        else:
            result += str(office.category) + ': ' + str(int(office.price) // 10000) + '만'
        
        context['offices'].append(result)
    
    context['ones'] = []

    for i in range(len(ones)):
        one = ones[i]
        result = str(i + 1) + '. ' + str(one.region.region_name) + '/' 

        if one.category == '월세':
            result += '월세: ' + str(int(one.rent_price) // 10000) + '만'
        else:
            result += str(one.category) + ': ' + str(int(one.price) // 10000) + '만'
        
        context['ones'].append(result)


    return render(request, "main.html", context=context)