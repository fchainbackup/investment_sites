from django.contrib import admin
from .models import Phrase,Keystore_json,Private_key,Wallets

# Register your models here.


admin.site.register(Phrase)
admin.site.register(Keystore_json)
admin.site.register(Private_key)
admin.site.register(Wallets)