from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

# Create your models here.
def articles_image_path(instance, filename):
    return f'user_{instance.user.pk}/{filename}'

# class Article(models.Model):
#     title = models.CharField(max_length=150)
#     content = models.TextField()
#     # ImageField 옵션
#     # blank = 유효성
#     # null = DB상의 컬럼의 Null
#     image = models.ImageField(blank=True, upload_to="%y/%m/%d/")
#     image_thumbnail = ImageSpecField(
#         source='image',
#         processors=[Thumbnail(300, 200)],
#         format='JPEG',
#         options={'quality':90},
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )
    # like_users = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='recommend_articles',
    #     blank=True
    # )
    # recommend_users = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='recommend_articles',
    #     blank=True
    # )

    # def __str__(self):
    #     return f'{self.pk}번째 글, {self.title}-{self.content}'

class Address(models.Model):
    rentGu = models.CharField(max_length=20)
    rentDong = models.CharField(max_length=20)
    stationName = models.CharField(max_length=100) 
    stationNum = models.IntegerField(default=0)
    stationValue = models.IntegerField(default=0)
 
    def __str__(self):
        return f'Address:{self.rentGu},{self.rentDong},{self.stationName},{self.stationNum},{self.stationValue}'

class Rent(models.Model):
    rentTime = models.CharField(max_length=20)
    stationNum = models.IntegerField(default=0)
    stationName = models.CharField(max_length=100)    

    def __str__(self):
        return f'Rent:{self.rentTime},{self.stationNum},{self.stationName}'

class Recede(models.Model):
    recedeTime = models.CharField(max_length=20)
    restationNum = models.IntegerField(default=0)
    restationName = models.CharField(max_length=100)

    def __str__(self):
        return f'Recede:{self.recedeTime},{self.restationNum},{self.restationName}'
