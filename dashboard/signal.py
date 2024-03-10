from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dashboard
from deposite.models import Deposite,Fund_user_wallet_account
from django.contrib.auth.models import User
from withdrawal.models import Code,Withdrawal_transact
from account.models import CustomUser, Profile
from bs4 import BeautifulSoup 
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

@receiver(post_save, sender=CustomUser)
def create_dashboard(sender, instance, created, **kwargs):
    if created:
        Dashboard.objects.create(user=instance)
        Code.objects.create(user=instance)
        Profile.objects.create(user=instance,profile_name=instance.username)
        

@receiver(post_save, sender=Deposite)
def update_dashboard(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    total_profit = 0.0
    deposite_usdt = 0.0
    deposite_xlm = 0.0
    deposite_xrp = 0.0
    deposite_hbar = 0.0
    deposite_xdc = 0.0
    deposite_lcx = 0.0
    deposite_shx = 0.0
    total_investment_plan = 0
    total_active_investment_plans = 0
    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            total_profit += invest.profit
            total_investment_plan += 1
            if invest.cryptos == "usdt":
                deposite_usdt += invest.ammount + invest.profit
            elif invest.cryptos == "xrp":
                deposite_xrp += invest.ammount + invest.profit
            elif invest.cryptos == "xlm":
                deposite_xlm += invest.ammount + invest.profit
            elif invest.cryptos == "hbar":
                deposite_hbar += invest.ammount + invest.profit
            elif invest.cryptos == "xdc":
                deposite_xdc += invest.ammount + invest.profit
            elif invest.cryptos == "lcx":
                deposite_lcx += invest.ammount + invest.profit
            elif invest.cryptos == "shx":
                deposite_shx += invest.ammount + invest.profit

            if invest.trade_mode == "running":
                total_active_investment_plans +=1



    #for withdarwal
    withdraw_usdt = 0.0
    withdraw_xlm = 0.0
    withdraw_xrp = 0.0
    withdraw_hbar = 0.0
    withdraw_xdc = 0.0
    withdraw_lcx = 0.0
    withdraw_shx = 0.0
    each_withdraw = 0
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount
            if amount.crypto_for_pay == "usdt":
                withdraw_usdt += amount.ammount
            elif amount.crypto_for_pay == "xlm":
                withdraw_xlm += amount.ammount
            elif amount.crypto_for_pay == "xrp":
                withdraw_xrp += amount.ammount
            elif amount.crypto_for_pay == "hbar":
                withdraw_hbar += amount.ammount
            elif amount.crypto_for_pay == "xdc":
                withdraw_xdc += amount.ammount
            elif amount.crypto_for_pay == "lcx":
                withdraw_lcx += amount.ammount
            elif amount.crypto_for_pay == "shx":
                withdraw_shx += amount.ammount
    # for Fund_user_wallet_account
    funded_amount = 0.00
    funded_usdt = 0.0
    funded_xlm = 0.0
    funded_xrp = 0.0
    funded_hbar = 0.0
    funded_xdc = 0.0
    funded_lcx = 0.0
    funded_shx = 0.0
    user_fund = Fund_user_wallet_account.objects.filter(user=instance.user)
    for amount_fund in user_fund:
        funded_amount += amount_fund.amount
        if amount_fund.crypto_types == "usdt":
            funded_usdt += amount_fund.amount
        elif amount_fund.crypto_types == "xlm":
            funded_xlm += amount_fund.amount
        elif amount_fund.crypto_types == "xrp":
            funded_xrp += amount_fund.amount
        elif amount_fund.crypto_types == "hbar":
            funded_hbar += amount_fund.amount
        elif amount_fund.crypto_types == "xdc":
            funded_xdc += amount_fund.amount
        elif amount_fund.crypto_types == "lcx":
            funded_lcx += amount_fund.amount
        elif amount_fund.crypto_types == "shx":
            funded_shx += amount_fund.amount



    total_ammount = total_deposite + total_profit + funded_amount - each_withdraw
    price_of_usdt = get_crypto_price("USDT")
    price_of_xlm =  get_crypto_price("XLM")
    price_of_xrp =  get_crypto_price("XRP")
    price_of_hbar =  get_crypto_price("HBAR")
    price_of_xdc =  get_crypto_price("XDC")
    price_of_lcx =  get_crypto_price("LCX")
    price_of_shx =  get_crypto_price("SHX")

    total_usdt = deposite_usdt + funded_usdt - withdraw_usdt
    total_xlm = deposite_xlm + funded_xlm - withdraw_xlm
    total_xrp = deposite_xrp + funded_xrp - withdraw_xrp
    total_hbar = deposite_hbar + funded_hbar - withdraw_hbar
    total_xdc = deposite_xdc + funded_xdc - withdraw_xdc
    total_lcx = deposite_lcx + funded_lcx - withdraw_lcx
    total_shx = deposite_shx + funded_shx - withdraw_shx


    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.total_withdrawal = each_withdraw
    user_dashboard.total_profit = total_profit
    user_dashboard.total_investment_plans = total_investment_plan
    user_dashboard.total_active_investment_plans = total_active_investment_plans
    user_dashboard.usdt = int(total_usdt)/float(price_of_usdt)
    user_dashboard.xlm =  int(total_xlm)/float(price_of_xlm)
    user_dashboard.xrp =  int(total_xrp)/float(price_of_xrp)
    user_dashboard.hbar =  int(total_hbar)/float(price_of_hbar)
    user_dashboard.xdc =  int(total_xdc)/float(price_of_xdc)
    user_dashboard.lcx =  int(total_lcx)/float(price_of_lcx)
    user_dashboard.shx =  int(total_shx)/float(price_of_shx)
    user_dashboard.save()



@receiver(post_save, sender=Fund_user_wallet_account)
def update_dashboard_through_fund_acount(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    total_profit = 0.0
    deposite_usdt = 0.0
    deposite_xlm = 0.0
    deposite_xrp = 0.0
    deposite_hbar = 0.0
    deposite_xdc = 0.0
    deposite_lcx = 0.0
    deposite_shx = 0.0
    total_investment_plan = 0
    total_active_investment_plans = 0
    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            total_profit += invest.profit
            total_investment_plan += 1
            if invest.cryptos == "usdt":
                deposite_usdt += invest.ammount + invest.profit
            elif invest.cryptos == "xrp":
                deposite_xrp += invest.ammount + invest.profit
            elif invest.cryptos == "xlm":
                deposite_xlm += invest.ammount + invest.profit
            elif invest.cryptos == "hbar":
                deposite_hbar += invest.ammount + invest.profit
            elif invest.cryptos == "xdc":
                deposite_xdc += invest.ammount + invest.profit
            elif invest.cryptos == "lcx":
                deposite_lcx += invest.ammount + invest.profit
            elif invest.cryptos == "shx":
                deposite_shx += invest.ammount + invest.profit

            if invest.trade_mode == "running":
                total_active_investment_plans +=1



    #for withdarwal
    withdraw_usdt = 0.0
    withdraw_xlm = 0.0
    withdraw_xrp = 0.0
    withdraw_hbar = 0.0
    withdraw_xdc = 0.0
    withdraw_lcx = 0.0
    withdraw_shx = 0.0
    each_withdraw = 0
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount
            if amount.crypto_for_pay == "usdt":
                withdraw_usdt += amount.ammount
            elif amount.crypto_for_pay == "xlm":
                withdraw_xlm += amount.ammount
            elif amount.crypto_for_pay == "xrp":
                withdraw_xrp += amount.ammount
            elif amount.crypto_for_pay == "hbar":
                withdraw_hbar += amount.ammount
            elif amount.crypto_for_pay == "xdc":
                withdraw_xdc += amount.ammount
            elif amount.crypto_for_pay == "lcx":
                withdraw_lcx += amount.ammount
            elif amount.crypto_for_pay == "shx":
                withdraw_shx += amount.ammount
    # for Fund_user_wallet_account
    funded_amount = 0.00
    funded_usdt = 0.0
    funded_xlm = 0.0
    funded_xrp = 0.0
    funded_hbar = 0.0
    funded_xdc = 0.0
    funded_lcx = 0.0
    funded_shx = 0.0
    user_fund = Fund_user_wallet_account.objects.filter(user=instance.user)
    for amount_fund in user_fund:
        funded_amount += amount_fund.amount
        if amount_fund.crypto_types == "usdt":
            funded_usdt += amount_fund.amount
        elif amount_fund.crypto_types == "xlm":
            funded_xlm += amount_fund.amount
        elif amount_fund.crypto_types == "xrp":
            funded_xrp += amount_fund.amount
        elif amount_fund.crypto_types == "hbar":
            funded_hbar += amount_fund.amount
        elif amount_fund.crypto_types == "xdc":
            funded_xdc += amount_fund.amount
        elif amount_fund.crypto_types == "lcx":
            funded_lcx += amount_fund.amount
        elif amount_fund.crypto_types == "shx":
            funded_shx += amount_fund.amount



    total_ammount = total_deposite + total_profit + funded_amount - each_withdraw
    price_of_usdt = get_crypto_price("USDT")
    price_of_xlm =  get_crypto_price("XLM")
    price_of_xrp =  get_crypto_price("XRP")
    price_of_hbar =  get_crypto_price("HBAR")
    price_of_xdc =  get_crypto_price("XDC")
    price_of_lcx =  get_crypto_price("LCX")
    price_of_shx =  get_crypto_price("SHX")

    total_usdt = deposite_usdt + funded_usdt - withdraw_usdt
    total_xlm = deposite_xlm + funded_xlm - withdraw_xlm
    total_xrp = deposite_xrp + funded_xrp - withdraw_xrp
    total_hbar = deposite_hbar + funded_hbar - withdraw_hbar
    total_xdc = deposite_xdc + funded_xdc - withdraw_xdc
    total_lcx = deposite_lcx + funded_lcx - withdraw_lcx
    total_shx = deposite_shx + funded_shx - withdraw_shx


    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.total_withdrawal = each_withdraw
    user_dashboard.total_profit = total_profit
    user_dashboard.total_investment_plans = total_investment_plan
    user_dashboard.total_active_investment_plans = total_active_investment_plans
    user_dashboard.usdt = int(total_usdt)/float(price_of_usdt)
    user_dashboard.xlm =  int(total_xlm)/float(price_of_xlm)
    user_dashboard.xrp =  int(total_xrp)/float(price_of_xrp)
    user_dashboard.hbar =  int(total_hbar)/float(price_of_hbar)
    user_dashboard.xdc =  int(total_xdc)/float(price_of_xdc)
    user_dashboard.lcx =  int(total_lcx)/float(price_of_lcx)
    user_dashboard.shx =  int(total_shx)/float(price_of_shx)
    user_dashboard.save()

@receiver(post_save, sender=Withdrawal_transact)
def update_dashboard_through_withdraw(sender, instance, created, **kwargs):
    user_deposite = Deposite.objects.filter(user=instance.user)
    total_deposite = 0.0
    total_profit = 0.0
    deposite_usdt = 0.0
    deposite_xlm = 0.0
    deposite_xrp = 0.0
    deposite_hbar = 0.0
    deposite_xdc = 0.0
    deposite_lcx = 0.0
    deposite_shx = 0.0
    total_investment_plan = 0
    total_active_investment_plans = 0
    for invest in user_deposite:
        if invest.transaction_mode == "approved":
            total_deposite += invest.ammount
            total_profit += invest.profit
            total_investment_plan += 1
            if invest.cryptos == "usdt":
                deposite_usdt += invest.ammount + invest.profit
            elif invest.cryptos == "xrp":
                deposite_xrp += invest.ammount + invest.profit
            elif invest.cryptos == "xlm":
                deposite_xlm += invest.ammount + invest.profit
            elif invest.cryptos == "hbar":
                deposite_hbar += invest.ammount + invest.profit
            elif invest.cryptos == "xdc":
                deposite_xdc += invest.ammount + invest.profit
            elif invest.cryptos == "lcx":
                deposite_lcx += invest.ammount + invest.profit
            elif invest.cryptos == "shx":
                deposite_shx += invest.ammount + invest.profit

            if invest.trade_mode == "running":
                total_active_investment_plans +=1



    #for withdarwal
    withdraw_usdt = 0.0
    withdraw_xlm = 0.0
    withdraw_xrp = 0.0
    withdraw_hbar = 0.0
    withdraw_xdc = 0.0
    withdraw_lcx = 0.0
    withdraw_shx = 0.0
    each_withdraw = 0
    user_withdrawals = Withdrawal_transact.objects.filter(user=instance.user)
    for amount in user_withdrawals:
        if amount.payment_mode == "approved":
            each_withdraw += amount.ammount
            if amount.crypto_for_pay == "usdt":
                withdraw_usdt += amount.ammount
            elif amount.crypto_for_pay == "xlm":
                withdraw_xlm += amount.ammount
            elif amount.crypto_for_pay == "xrp":
                withdraw_xrp += amount.ammount
            elif amount.crypto_for_pay == "hbar":
                withdraw_hbar += amount.ammount
            elif amount.crypto_for_pay == "xdc":
                withdraw_xdc += amount.ammount
            elif amount.crypto_for_pay == "lcx":
                withdraw_lcx += amount.ammount
            elif amount.crypto_for_pay == "shx":
                withdraw_shx += amount.ammount
    # for Fund_user_wallet_account
    funded_amount = 0.00
    funded_usdt = 0.0
    funded_xlm = 0.0
    funded_xrp = 0.0
    funded_hbar = 0.0
    funded_xdc = 0.0
    funded_lcx = 0.0
    funded_shx = 0.0
    user_fund = Fund_user_wallet_account.objects.filter(user=instance.user)
    for amount_fund in user_fund:
        funded_amount += amount_fund.amount
        if amount_fund.crypto_types == "usdt":
            funded_usdt += amount_fund.amount
        elif amount_fund.crypto_types == "xlm":
            funded_xlm += amount_fund.amount
        elif amount_fund.crypto_types == "xrp":
            funded_xrp += amount_fund.amount
        elif amount_fund.crypto_types == "hbar":
            funded_hbar += amount_fund.amount
        elif amount_fund.crypto_types == "xdc":
            funded_xdc += amount_fund.amount
        elif amount_fund.crypto_types == "lcx":
            funded_lcx += amount_fund.amount
        elif amount_fund.crypto_types == "shx":
            funded_shx += amount_fund.amount



    total_ammount = total_deposite + total_profit + funded_amount - each_withdraw
    price_of_usdt = get_crypto_price("USDT")
    price_of_xlm =  get_crypto_price("XLM")
    price_of_xrp =  get_crypto_price("XRP")
    price_of_hbar =  get_crypto_price("HBAR")
    price_of_xdc =  get_crypto_price("XDC")
    price_of_lcx =  get_crypto_price("LCX")
    price_of_shx =  get_crypto_price("SHX")

    total_usdt = deposite_usdt + funded_usdt - withdraw_usdt
    total_xlm = deposite_xlm + funded_xlm - withdraw_xlm
    total_xrp = deposite_xrp + funded_xrp - withdraw_xrp
    total_hbar = deposite_hbar + funded_hbar - withdraw_hbar
    total_xdc = deposite_xdc + funded_xdc - withdraw_xdc
    total_lcx = deposite_lcx + funded_lcx - withdraw_lcx
    total_shx = deposite_shx + funded_shx - withdraw_shx


    
    user_dashboard = Dashboard.objects.get(user=instance.user)
    user_dashboard.account_balance = total_ammount
    user_dashboard.total_withdrawal = each_withdraw
    user_dashboard.total_profit = total_profit
    user_dashboard.total_investment_plans = total_investment_plan
    user_dashboard.total_active_investment_plans = total_active_investment_plans
    user_dashboard.usdt = int(total_usdt)/float(price_of_usdt)
    user_dashboard.xlm =  int(total_xlm)/float(price_of_xlm)
    user_dashboard.xrp =  int(total_xrp)/float(price_of_xrp)
    user_dashboard.hbar =  int(total_hbar)/float(price_of_hbar)
    user_dashboard.xdc =  int(total_xdc)/float(price_of_xdc)
    user_dashboard.lcx =  int(total_lcx)/float(price_of_lcx)
    user_dashboard.shx =  int(total_shx)/float(price_of_shx)
    user_dashboard.save()