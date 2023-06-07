from django.db import models
from django.contrib.auth.models import User
import random
from account.models import CustomUser
# Create your models here.
PAYMENT_MODE = (
    ('pending','pending'),
    ('approved','approved'),
)

class Withdrawal_transact(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ammount = models.FloatField()
    network =models.CharField(max_length=20,default="none")
    crypto_for_pay = models.CharField(max_length=20)
    crypto_address = models.CharField(max_length=200)
    payment_mode = models.CharField(max_length=13,choices=PAYMENT_MODE)
   
    def __str__(self):
        return str(self.user) +" - "+ str(self.ammount) 

class Code(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    otp = models.CharField(max_length=5,blank=True)
   
    def __str__(self):
        return str(self.user) +" - "+ str(self.otp)

    def save(self,*args,**kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.otp=code_string
        return super().save(*args,**kwargs)