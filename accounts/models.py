from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    name=models.CharField(verbose_name='名前', max_length=50)
    userType=models.CharField(verbose_name='ユーザタイプ', max_length=10)

    # 管理で必要な情報などを記述するクラス
    class Meta:
        # 管理サイトで表示されるモデル名
        verbose_name_plural = 'カスタムユーザ'

    def __str__(self):
        return self.email