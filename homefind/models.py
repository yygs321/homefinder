from django.db import models

class Region(models.Model):
    region_name = models.CharField(max_length=100)


class RealEstate(models.Model):
    price = models.FloatField(default=0)
    category = models.CharField(max_length=10)
    pyeongsu = models.IntegerField(default=0)
    house_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    spec_address = models.CharField(max_length=200)
    region = models.ForeignKey(Region, related_name='real_estates', on_delete=models.CASCADE)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.house_name

