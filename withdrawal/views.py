from django.shortcuts import render,redirect
from dashboard.models import Dashboard
from django.contrib import messages
from .models import Withdrawal_transact,Code
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.


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



def otp_verification_email(user,otp):
    
    email_subject = 'OTP withdrawal verification'
    email_body = render_to_string('withdrawal/otp_send_email.html', {
        'user': user,
        'otp':otp,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledger.com',
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()


def send_withdrawal_email_alert(user,amount,cypto,address,network):
    
    email_subject = 'User withdrawal'
    email_body = render_to_string('withdrawal/user_withdrawal_alert.html', {
        'user': user,
        'amount':amount,
        'cypto':cypto,
        'address':address,
        'network':network,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledger.com',
                         to=["johnsimonwork@gmail.com"]
                         )
    if not settings.TESTING:
        EmailThread(email).start()


@login_required
def user_withdrawal(request):
    
    user = request.user
    user_ballance= Dashboard.objects.get(user=user)
    account_balance = "not_available"
    if user_ballance.account_balance > 1:
        account_balance = "available"

        if request.method == 'POST':
            crypto = request.POST.get("format")
            network = request.POST.get("network")
            amount = request.POST.get("amount")
            address = request.POST.get("address")

            try:
                amount = int(amount)
                print(amount)
                if amount <= user_ballance.account_balance:
                    user_withdraws = Withdrawal_transact.objects.filter(user=request.user)
                    if user_withdraws is not None:
                        total_withdarw = amount
                        for wd in user_withdraws:
                            total_withdarw += wd.ammount
                        if total_withdarw <= user_ballance.account_balance:
                            request.session['withdrawal'] = {"crypto":crypto,"network":network,"amount":amount,"address":address}
                            user_otp = Code.objects.get(user=request.user)
                            user=request.user
                            otp_verification_email(user,user_otp)
                            return redirect('withdrawal:withdraw_verify')
                            
                        else:
                            messages.error(request, "you have exceeded your account balance limit")



                else:
                    messages.error(request, "not enough balance")
                    
            except:
                messages.error(request, "Enter a valid amount")
            




        return render(request,"withdrawal/withdraw.html",{"account_balance":account_balance})
    return render(request,"withdrawal/withdraw.html",{"account_balance":account_balance})

@login_required
def verification(request):
    user_email=request.user.email
    withdrawal = request.session.get('withdrawal')
    session = "not_available"
    if withdrawal is not None:
        session = "available"
        crypto = withdrawal["crypto"]
        network = withdrawal["network"]
        address = withdrawal["address"]
        amount = withdrawal["amount"]
        if request.method == 'POST':
            otp_code = request.POST.get("otp")
            user_otp = Code.objects.get(user=request.user)
            if user_otp.otp == otp_code:
                user_placed_withdraw=Withdrawal_transact(user=request.user,ammount=amount,network=network,crypto_for_pay=crypto,crypto_address=address,payment_mode="pending")
                user_placed_withdraw.save()
                user_otp.save()
                user=request.user
                send_withdrawal_email_alert(user,amount,crypto,address,network)
                del request.session['withdrawal']
                messages.success(request,"your withdrawal have been placed successfully!")
                return redirect('dashboard:dashboard-page')
                
            else:
                messages.error(request,"incorrect OTP try again")
        return render(request,"withdrawal/withdraw_rerify.html",{"user_email":user_email,"session":session})
    return render(request,"withdrawal/withdraw_rerify.html",{"user_email":user_email,"session":session})

def send_otp_json(request):
    user_otp = Code.objects.get(user=request.user)
    user=request.user
    otp_verification_email(user,user_otp)
    

    return JsonResponse({"sent":"ok"})

@login_required
def my_withdrawal(request):

    my_withdraw = Withdrawal_transact.objects.filter(user=request.user).order_by('-pk')
    transaction_found = "no"
    if my_withdraw.exists():

        transaction_found = "yes"

    return render(request,"withdrawal/my_withdrawal.html",{"my_withdraw":my_withdraw,"transaction_found":transaction_found})