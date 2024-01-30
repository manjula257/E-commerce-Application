from django.db import models
from django.contrib.auth.models import User

class Reg(models.Model):
    uname=models.EmailField(max_length=20)
    upass=models.CharField(max_length=20)
    ucpass=models.CharField(max_length=20)

class Log(models.Model):
    uname=models.EmailField(max_length=20)
    upass=models.CharField(max_length=20)

class product(models.Model):
    pname=models.CharField(max_length=50)
    pcost=models.FloatField()
    pdetails=models.CharField(max_length=100)
    cat=models.IntegerField()
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image/')
    def __str__(self):
        return self.pname
    
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

