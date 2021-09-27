from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserInfo(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        '用户名',
        max_length=26,
        unique=True
    )
    password = models.CharField(
        '密码',
        max_length=128
    )
    created = models.DateTimeField(auto_now_add=True)
    matrix = models.CharField(max_length=128,null=True,blank=True,default=None)
