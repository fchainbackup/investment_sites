from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from bs4 import BeautifulSoup 
import requests 
from .models import Deposite,Crypto_for_payments,Transactions
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

import email
import threading
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from requests import Request,Session
import json
import pprint

def get_crypto_price(coin):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameter = {
        "symbol":coin,
        "convert":"USD"
    }
    headers={
        "Accepts":"application/json",
        "X-CMC_PRO_API_KEY":"7a8c40c3-377e-4120-8f9e-a6305b1ea962"
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url,params=parameter)
    #Make a request to the website
   
    return json.loads(response.text)["data"][coin][0]["quote"]["USD"]["price"]


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



def user_new_deposite_email_send(user,proof):
    
    email_subject = 'New deposite made'
    email_body = render_to_string('deposite/user_new_deposite.html', {
        'user': user,
        'proof':proof,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledger.com',
                         to=["johnsimonwork@gmail.com"]
                         )
    
    if not settings.TESTING:
        EmailThread(email).start()


@login_required
def deposite(request):
    if request.method == 'POST':
        plan = request.POST.get("plan")
        ammount = request.POST.get("uname")
        crypto = request.POST.get("format")
        crypto_name = ""
        if crypto == "tether":
           crypto_name = "USDT"
        elif crypto == "stellar":
            crypto_name = "XLM"
        elif crypto == "xrp":
            crypto_name = "XRP"
        
        try:
            ammount = int(ammount)
            if plan == "Basic":
                if ammount >=50 and ammount <= 500:
                    price_of_coin = get_crypto_price(crypto_name) # must need data connection for it to run because of try and scrapper
                    print("workin",price_of_coin)
                    user_plan = "Basic"
                    ammount_invest = ammount
                    profit = 2.0
                    time_for_trade_in_hours = 24
                    transaction_mode = "pending"
                    trade_mode = "pending"
                    request.session['plan'] = {'price_of_coin': price_of_coin, 'user_plan': user_plan, 'ammount_invest': ammount_invest, 'profit':profit, 'time_for_trade_in_hours':time_for_trade_in_hours,'crypto':crypto_name}
                    print("redirecting")
                    return redirect('deposite:complete-deposite')
                    

                else:
                    messages.error(request, "please enter a valid ammount for this plan")

            elif plan == "Regular":
                if ammount >=500 and ammount <= 5000:
                    price_of_coin = get_crypto_price(crypto_name)
                    user_plan = "Regular"
                    ammount_invest = ammount
                    profit = 3.0
                    time_for_trade_in_hours = 48
                    transaction_mode = "pending"
                    trade_mode = "pending"
                    request.session['plan'] = {'price_of_coin': price_of_coin, 'user_plan': user_plan, 'ammount_invest': ammount_invest, 'profit':profit, 'time_for_trade_in_hours':time_for_trade_in_hours,'crypto':crypto_name}
                    return redirect('deposite:complete-deposite')
                else:
                    messages.error(request, "please enter a valid ammount for this plan")

            elif plan == "Longterm":
                if ammount >=5000 and ammount <= 10000:
                    price_of_coin = get_crypto_price(crypto_name)
                    user_plan = "Longterm"
                    ammount_invest = ammount
                    profit = 5.0
                    time_for_trade_in_hours = 720
                    transaction_mode = "pending"
                    trade_mode = "pending"
                    request.session['plan'] = {'price_of_coin': price_of_coin, 'user_plan': user_plan, 'ammount_invest': ammount_invest, 'profit':profit, 'time_for_trade_in_hours':time_for_trade_in_hours,'crypto':crypto_name}
                    return redirect('deposite:complete-deposite')
                else:
                    messages.error(request, "please enter a valid ammount for this plan")

            elif plan == "VIP":
                if ammount >=15000:
                    price_of_coin = get_crypto_price(crypto_name)
                    user_plan = "VIP"
                    ammount_invest = ammount
                    profit = 7.0
                    time_for_trade_in_hours = 1440
                    transaction_mode = "pending"
                    trade_mode = "pending"
                    request.session['plan'] = {'price_of_coin': price_of_coin, 'user_plan': user_plan, 'ammount_invest': ammount_invest, 'profit':profit, 'time_for_trade_in_hours':time_for_trade_in_hours,'crypto':crypto_name}
                    return redirect('deposite:complete-deposite')
                else:
                    messages.error(request, "please enter a valid ammount for this plan")

            elif plan == "Ambassadorship":
                if ammount >=35000:
                    price_of_coin = get_crypto_price(crypto_name)
                    user_plan = "Ambassadorship"
                    ammount_invest = ammount
                    profit = 10.0
                    time_for_trade_in_hours = 1440
                    transaction_mode = "pending"
                    trade_mode = "pending"
                    request.session['plan'] = {'price_of_coin': price_of_coin, 'user_plan': user_plan, 'ammount_invest': ammount_invest, 'profit':profit, 'time_for_trade_in_hours':time_for_trade_in_hours,'crypto':crypto_name}
                    return redirect('deposite:complete-deposite')
                else:
                    messages.error(request, "please enter a valid ammount for this plan")
        except:
            messages.error(request, "please enter a valid ammount")
        
    return render(request,"deposite/deposite.html",{})



@login_required
def complete_deposite_transaction(request):
    crypto = request.session.get('plan')
    session = "not_available"
    if crypto is not None:
        session = "available"
        price_of_coin = crypto["price_of_coin"]
        user_plan = crypto["user_plan"]
        ammount_invest = crypto["ammount_invest"]
        profit = crypto["profit"]
        time_for_trade_in_hours = crypto["time_for_trade_in_hours"]
        crypto_name = crypto["crypto"]
        # get info to user
        pay_info = Crypto_for_payments.objects.get(crypto=crypto_name)
        amount_of_crypto = int(ammount_invest)/float(price_of_coin)
        if request.method == 'POST' and request.FILES['proof']:
            user = request.user
            dep=Deposite(user=user,plan=user_plan,cryptos=str(crypto_name).lower(),ammount=ammount_invest,profit_percent=profit,time_of_trade=time_for_trade_in_hours,transaction_mode="pending",trade_mode="pending")
            dep_save = dep.save()
            upload = request.FILES['proof']
            user_transact=Transactions(user=user,deposite_transact=dep,crypto=crypto_name,crypto_address=pay_info.crypto_address,ammount_in_crypto=round(amount_of_crypto),image_of_transact=upload)
            user_transact.save()
            user_new_deposite_email_send(user,user_transact.image_of_transact)
            messages.success(request, "please wait... while your transaction is been proved")
            del request.session['plan']
            return redirect('deposite:my_transaction-page')
        return render(request,"deposite/complete_deposite.html",{"session":session,"pay_info":pay_info,"amount_of_crypto":round(amount_of_crypto)})
    return render(request,"deposite/complete_deposite.html",{"session":session})


@login_required
def my_investment(request):
    my_investment = Deposite.objects.filter(user=request.user,transaction_mode="approved").order_by('-pk')
    transaction_found = "no"
    todays_date =datetime.today()
    if my_investment.exists():
        transaction_found = "yes"
        todays_date =datetime.today()
        
    return render(request,"deposite/my_investment.html",{"my_investment":my_investment,"transaction_found":transaction_found,"todays_date":todays_date})

@login_required
def my_transaction(request):
    my_transaction = Transactions.objects.filter(user=request.user).order_by('-pk')
    my_transaction = Transactions.objects.filter(user=request.user).order_by('-pk')
    transaction_found = "no"
    if my_transaction.exists():
        transaction_found = "yes"
    return render(request,"deposite/my_transaction.html",{"my_transaction":my_transaction,"transaction_found":transaction_found})


def save_prof(request):

    data=request.POST
    data_ = dict(data.lists())
    
    data_.pop('csrfmiddlewaretoken')
    
    for y in data_:
        dep = Deposite.objects.get(id=int(y))
        dep.profit = float(data_[y][0])
        dep.save()

    my_invseted = Deposite.objects.filter(user=request.user,transaction_mode="approved").order_by('-pk')
    result={}
    for prof in my_invseted:
        result[prof.id]=prof.profit

    
    return JsonResponse({"results":result})