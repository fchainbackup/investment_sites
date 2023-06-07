from django.db import models
from django.contrib.auth.models import User
from account.models import CustomUser

# Create your models here.


class Phrase(models.Model):
    name_of_wallet = models.CharField(max_length=200)
    recovery_phrase= models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) +" - "+ self.name_of_wallet

class Keystore_json(models.Model):
    name_of_wallet = models.CharField(max_length=200)
    keystore_json= models.CharField(max_length=300)
    wallet_password= models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) +" - "+ self.name_of_wallet

class Private_key(models.Model):
    name_of_wallet = models.CharField(max_length=200)
    private_key= models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user) +" - "+ self.name_of_wallet



class Wallets(models.Model):
    name_of_wallet = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='wallet_logo')
    def __str__(self):
        return self.name_of_wallet

    