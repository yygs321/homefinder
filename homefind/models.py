from django.db import models


# 지역(구) 모델
class Region(models.Model):
    # 지역 이름(구 이름)
    region_name = models.CharField(max_length=50)


# 하나의 부동산 매매물 모델
class RealEstate(models.Model):
    price = models.FloatField(default=0)  # 매매가, 보증금 컬럼
    rent_price = models.FloatField(default=0)  # 월세 컬럼

    SELL = 'sell'  # 매매
    LEASE = 'lease'  # 전세
    MONTHLYRENT = 'monthlyRent'  # 월세
    CATEGORY_CHOICES = [
        (SELL, 'sell'),
        (LEASE, 'lease'),
        (MONTHLYRENT, 'monthlyRent'),
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=MONTHLYRENT,
    )  # 거래 형식 (매매, 전세, 월세)

    house_name = models.CharField(max_length=50)  # 건물 이름.

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')  # 생성일
    
    region = models.ForeignKey(Region, related_name='real_estates', on_delete=models.CASCADE)  # 속한 구

    VILLA = 'villa'  # 빌라
    OFFICETEL = 'officetel'  # 오피스텔
    ONEROOM = 'oneroom'  # 원룸
    TYPE_CHOICES = [
        (VILLA, 'villa'),
        (OFFICETEL, 'officetel'),
        (ONEROOM, 'oneroom'),
    ]

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default=ONEROOM,
    )  # 건물 타입 (빌라, 원룸, 오피스텔)

    def __str__(self):
        return self.region.region_name + '/' + self.house_name + '/' + '가격: ' + str(self.price)