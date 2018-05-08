from django.db import models

class CartInfo(models.Model):
    #关联的其他应用的模型类写法
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField()

