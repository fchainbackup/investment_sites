from django.contrib import admin
from .models import Deposite,Transactions,Crypto_for_payments,Fund_user_wallet_account
# Register your models here.



admin.site.register(Fund_user_wallet_account)
admin.site.register(Deposite)
admin.site.register(Transactions)
admin.site.register(Crypto_for_payments)
