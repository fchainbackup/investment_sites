import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
# Create your models here.



class CustomUser(AbstractUser):
    email = models.CharField(_('email address'),max_length=150,unique=True)
    is_email_verified= models.BooleanField(default=False)
    nationality = CountryField(blank_label='(select country)')
    phone_number = models.CharField(_('phone number'),max_length=12,blank=True)




class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_name = models.CharField(_('name'),max_length=100,blank=True)
    recommended_by = models.ForeignKey(CustomUser,blank=True,null=True,on_delete=models.CASCADE,related_name="ref_by")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.profile_name) 
    

    

    