from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail


# Create your models here.
def notices_image_path(instance, filename):
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
    stationNum = models.IntegerField(default=0, primary_key=True)
    stationValue = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['rentGu']
    
    def __str__(self):
        return f'Address:{self.rentGu},{self.rentDong},{self.stationName},{self.stationNum},{self.stationValue}'
    
class Rent(models.Model):
    rentTime = models.DateTimeField()
    stationNum = models.ForeignKey(
        Address,
        on_delete=models.CASCADE
    )
    stationName = models.CharField(max_length=100)
    class Meta:
        ordering = ['rentTime']
    def __str__(self):
        return f'Rent:{self.rentTime},{self.stationNum},{self.stationName}'

class Recede(models.Model):
    recedeTime = models.DateTimeField()
    stationNum = models.ForeignKey(
        Address,
        on_delete=models.CASCADE
    )
    stationName = models.CharField(max_length=100)
    class Meta:
        ordering = ['recedeTime']
    def __str__(self):
        return f'Recede:{self.recedeTime},{self.stationNum},{self.stationName}'

# 공지사항 model
class Notice(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to=notices_image_path)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(400,500)],
        format='JPEG',
        options={'quality':90}
    )
    upload = models.FileField(blank=True, upload_to=notices_image_path, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    # 멤버 변수 = models.외래키(참조하는 객체, 삭제 되었을 때 처리 방법)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    # 역참조 값 설정 related_name='comments'
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Notice:{self.notice}, {self.pk}-{self.content}'