import os

from django.db import models

from apps.users.models import User
from system.storage import ImageStorage
from utils.modles import BaseModel
# Create your models here.

# def user_directory_path(filename):
#     import time
#     import random
#     temp = time.time()
#     ext = filename.split('.').pop()
#     name = filename.split('.')[0]
#     filename = '{0}{1}{2}.{3}'.format(temp,random.randint(100),name,ext)
#     path_str = '/static/trends_image/'
#     return os.path.join(path_str, filename)

class Channel(BaseModel):
    channel_name = models.CharField(max_length=32,verbose_name="频道名")

    class Meta:
        db_table = 'trends_channel'
        verbose_name = '频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.channel_name
class ImgInfo(BaseModel):
    trends_id = models.ForeignKey('Trends', on_delete=models.CASCADE,verbose_name="文章id")
    img = models.ImageField(upload_to='trends_image/%Y/%m/%d',storage=ImageStorage(),verbose_name="图片")

    class Meta:
        db_table = 'trends_image'
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.img

class Attitude(BaseModel):
    TREND_ATTITUDE = (
        (1, '赞'),
        (2, '踩')
    )
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    trends_id = models.ForeignKey('Trends',on_delete=models.CASCADE,verbose_name="文章")
    attitude = models.SmallIntegerField(choices=TREND_ATTITUDE,verbose_name="评价")

    class Meta:
        db_table = 'trends_attitude'
        verbose_name = '文章评价'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Trends(BaseModel):
    title = models.CharField(max_length=1000, verbose_name="标题")
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    comment_count = models.IntegerField(default=0,verbose_name="评论数")
    likes_count = models.IntegerField(default=0,verbose_name="点赞数")
    content = models.TextField(default="如题", verbose_name="正文")
    channel_id = models.ForeignKey(Channel,on_delete=models.PROTECT,verbose_name="频道")
    # img_id = models.ForeignKey(ImgInfo,null=True,on_delete=models.SET_NULL,verbose_name="图片")

    class Meta:
        db_table = 'trends_info'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Commit(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    trends_id = models.ForeignKey(Trends, on_delete=models.CASCADE, verbose_name="文章")
    conent = models.TextField(max_length=9999,verbose_name="评论")

    class Meta:
        db_table = 'trends_commit'
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.conent