from django.db import models


# 지역(구) 모델
class Region(models.Model):
    # 지역 이름(구 이름)
    region_name = models.CharField(max_length=50)

    def __str__(self):
        return self.region_name


# 하나의 부동산 매매물 모델
class RealEstate(models.Model):
    price = models.FloatField(default=0)  # 매매가, 보증금 컬럼
    rent_price = models.FloatField(default=0)  # 월세 컬럼

    SELL = '매매'  # 매매
    LEASE = '전세'  # 전세
    MONTHLYRENT = '월세'  # 월세
    CATEGORY_CHOICES = [
        (SELL, '매매'),
        (LEASE, '전세'),
        (MONTHLYRENT, '월세'),
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=MONTHLYRENT,
    )  # 거래 형식 (매매, 전세, 월세)

    house_name = models.CharField(max_length=50)  # 건물 이름.

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')  # 생성일
    
    region = models.ForeignKey(Region, related_name='real_estates', on_delete=models.CASCADE)  # 속한 구

    VILLA = '빌라'  # 빌라
    OFFICETEL = '오피스텔'  # 오피스텔
    ONEROOM = '원룸'  # 원룸
    TYPE_CHOICES = [
        (VILLA, '빌라'),
        (OFFICETEL, '오피스텔'),
        (ONEROOM, '원룸'),
    ]

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default=ONEROOM,
    )  # 건물 타입 (빌라, 원룸, 오피스텔)

    def __str__(self):
        return self.region.region_name + '/' + self.house_name + '/' + self.type + '/' + self.category + '/' + '가격: ' + str(self.price)

# 뉴스 토픽 빈도수 모델
class NewsFrequency(models.Model):
    category = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
    count = models.IntegerField()
    date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')  # 생성일

    def __str__(self):
        return f"{self.category} - {self.value} on {self.date}"