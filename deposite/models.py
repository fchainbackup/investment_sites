from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
import time
from datetime import datetime, timedelta
from account.models import CustomUser
# Create your models here.

DIFF_CHOICES_TRADE_MODE = (
    ('running','running'),
    ('pending','pending'),
    ('completed','completed'),
)

DIFF_CHOICES_TRANS_MODE = (
    ('pending','pending'),
    ('approved','approved'),
)
 
CRYPTO_CHOICE= (
    ('usdt','USDT'),
    ('xrp','XRP'),
    ('xlm','XLM'),
)
class Deposite(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    plan = models.CharField(max_length=200)
    ammount = models.FloatField()
    profit_percent = models.FloatField()
    time_count_for_trade = models.IntegerField(default=0)
    time_of_trade = models.CharField(max_length=120)
    transaction_mode = models.CharField(max_length=11,choices=DIFF_CHOICES_TRANS_MODE)
    trade_mode = models.CharField(max_length=11,choices=DIFF_CHOICES_TRADE_MODE)
    profit = models.FloatField(default=0.00)
    cryptos = models.CharField(max_length=7,default="usdt")
    
    date_created =  models.DateTimeField(auto_now_add=True)
    date_of_trade =  models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return str(self.user) +" - "+ self.plan + "-" + str(self.ammount)

    

    def save(self,*args,**kwargs):
        if self.transaction_mode == "approved" and self.date_of_trade==None:
            if self.plan == "Basic" and self.date_of_trade==None:
                now = datetime.today()
                result = now + timedelta(hours=24)
                self.date_of_trade = result
                self.trade_mode = "running"
            elif self.plan =="Regular" and self.date_of_trade==None:
                now = datetime.today()
                result = now + timedelta(hours=48)
                self.date_of_trade = result
                self.trade_mode = "running"
            elif self.plan =="Longterm" and self.date_of_trade==None:
                now = datetime.today()
                result = now + timedelta(hours=720)
                self.date_of_trade = result
                self.trade_mode = "running"
            elif self.plan =="VIP" and self.date_of_trade==None:
                now = datetime.today()
                result = now + timedelta(hours=1440)
                self.date_of_trade = result
                self.trade_mode = "running"
            elif self.plan =="Ambassadorship" and self.date_of_trade==None:
                now = datetime.today()
                result = now + timedelta(hours=1440)
                self.date_of_trade = result
                self.trade_mode = "running"
            # for testing purpose    
        elif self.transaction_mode == "approved" and self.date_of_trade is not None:
           
            now_date = datetime.today()
            now_for_date = str(now_date).split(".")[0]
            trade_for_date = str(self.date_of_trade).split("+")[0]
            trade_for_date = trade_for_date.split(".")[0]
            print(now_for_date)
            print(trade_for_date)
            convert_to_date_now = datetime.strptime(now_for_date, '%Y-%m-%d %H:%M:%S')


            convert_to_date_trade = datetime.strptime(trade_for_date, '%Y-%m-%d %H:%M:%S')
            total_profit = (float(self.profit_percent)/100) * float(self.ammount)
            
            if convert_to_date_now >= convert_to_date_trade:
                self.profit = total_profit
                self.trade_mode = "completed"
    
        else:
            self.trade_mode = "pending"

            
        return super().save(*args,**kwargs)

    
    



class Transactions(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    deposite_transact = models.ForeignKey(Deposite,on_delete=models.CASCADE)
    crypto = models.CharField(max_length=200)
    crypto_address = models.CharField(max_length=200)
    ammount_in_crypto= models.FloatField()
    image_of_transact = models.ImageField(upload_to='verify_transact')
    date_created =  models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.deposite_transact) +" - "+ self.crypto + "-" + str(self.ammount_in_crypto)



class Crypto_for_payments(models.Model):
    crypto = models.CharField(max_length=200)
    crypto_address = models.CharField(max_length=200)
    network = models.CharField(max_length=200,default="none")
   
    def __str__(self):
        return str(self.crypto) +" - "+ self.crypto_address 


class Fund_user_wallet_account(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    amount = models.FloatField()
    crypto_types = models.CharField(max_length=5,choices=CRYPTO_CHOICE, default="xrp")
    date_created =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) +" funded "+ str(self.amount)


