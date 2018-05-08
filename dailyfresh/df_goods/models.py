from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
       return self.ttitle

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    #上传的文件存储到df_goods
    gpic = models.ImageField(upload_to='df_goods')
    #明确控制有几位数，max_digits一共包含多少位数，decimal_places表示有几位小数
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    #单位
    gunit = models.CharField(max_length=20, default='500g')
    #点击量
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo)


