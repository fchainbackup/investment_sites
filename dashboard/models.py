from django.db import models
from django.contrib.auth.models import User
from account.models import CustomUser

# Create your models here.

class Dashboard(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    account_balance = models.FloatField(default=0.00)
    usdt = models.FloatField(default=0.00)
    xrp = models.FloatField(default=0.00)
    xlm = models.FloatField(default=0.00)
    hbar = models.FloatField(default=0.00)
    xdc = models.FloatField(default=0.00)
    lcx = models.FloatField(default=0.00)
    shx = models.FloatField(default=0.00)
    total_profit = models.FloatField(default=0.00)
    total_bonus = models.FloatField(default=0.00)
    total_referal_bonus = models.FloatField(default=0.00)
    total_investment_plans = models.IntegerField(default=0)
    total_active_investment_plans = models.IntegerField(default=0)
    total_withdrawal = models.FloatField(default=0.00)
    def __str__(self):
        return str(self.user) +" - " + str(self.account_balance)