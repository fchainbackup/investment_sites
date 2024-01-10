from django.shortcuts import render
from .models import Dashboard
from account.models import Profile
from django.contrib.auth.decorators import login_required
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
   
    try:
        result = json.loads(response.text)["data"][coin][0]["quote"]["USD"]["price"]

        
    except Exception as error:
        result = 0
        
   
    return result

# Create your views here.
@login_required
def dashboard(request):
    user = request.user
    user_dashboard = Dashboard.objects.get(user=user)
    profile_name = Profile.objects.get(user=user)
    usdt_usd = float(get_crypto_price("USDT")) * float(user_dashboard.usdt)
    xlm_usd = float(get_crypto_price("XLM")) * float(user_dashboard.xlm)
    xrp_usd = float(get_crypto_price("XRP")) * float(user_dashboard.xrp)
    hbar_usd = float(get_crypto_price("HBAR")) * float(user_dashboard.hbar)
    xdc_usd = float(get_crypto_price("XDC")) * float(user_dashboard.xdc)
    lcx_usd = float(get_crypto_price("LCX")) * float(user_dashboard.lcx)
    referral = "https://assetssecurityledgers.com/account/ref/"+str(profile_name.profile_name)
    return render(request,"dashboard/dash.html",{"user_dashboard":user_dashboard,"referral":referral,"usdt":usdt_usd,"xlm":xlm_usd,"xrp":xrp_usd,"hbar":hbar_usd,"xdc":xdc_usd,"lcx":lcx_usd})