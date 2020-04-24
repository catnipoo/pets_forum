from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.modles import BaseModel
# Create your models here.

class User(AbstractUser):
    # 自定义用户模型类
    # user_id = models.AutoField(max_length=8,unique=True,verbose_name="用户id")
    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号")
    status = models.BooleanField(default=True,verbose_name="帐号状态")
    default_image = models.CharField(default='img/default_avatar',verbose_name='默认头像')
    following_count = models.IntegerField(default=0,verbose_name="关注数")
    articl_count = models.IntegerField(default=0,verbose_name="文章数")
    fans_count = models.IntegerField(default=0,verbose_name="粉丝数")



    class Meta:
        db_table = 'user_information'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class UserRelation(BaseModel):
    RELATION_STATUS = (
        (1,'关注'),
        (2,'取消关注')
    )
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    target_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="目标用户")
    status = models.SmallIntegerField(choices=RELATION_STATUS,verbose_name="用户关系")

    class Meta:
        db_table = 'user_relation'
        verbose_name = '用户关系'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
