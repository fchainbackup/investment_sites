from django.urls import path
from .views import user_withdrawal,verification,my_withdrawal,send_otp_json



app_name = "withdrawal"

urlpatterns = [
    path('', user_withdrawal,name="user_withdraw"),
    path('verify/', verification,name="withdraw_verify"),
    path('my_withdrawal/', my_withdrawal,name="withdrawals"),
    path('send_otp_json/', send_otp_json,name="send_otp"),

]
