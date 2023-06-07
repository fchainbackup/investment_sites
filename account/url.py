from django.urls import path
from .views import register_user,login_user,activate_user_email,forget_password,reset_password,to_reset_password,referral,logout_view,account_setting,support
from .views import home_page,about_page,contact_page,faq_page,tc_page


app_name = "account"

urlpatterns = [
    path('register_user',register_user,name="register_user" ),
    path('login_user',login_user,name="login_user" ),
    path('activate_user/<uidb64>/<token>', activate_user_email, name='activate'),
    path('forget_password/', forget_password, name='forget_password'),
    path('reset/<uidb64>/<token>', reset_password, name='reset_pass'),
    path('reset_password/', to_reset_password, name='to_reset_pass'),
    path('ref/<str:ref_code>/', referral, name='ref'),
    path('logout/', logout_view, name='logout'),
    path('account_setting/', account_setting, name='account_setting'),
    path('support/', support, name='support'),
    # home pages
    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('contact/', contact_page, name='contact_page'),
    path('faq/', faq_page, name='faq_page'),
    path('t&c/', tc_page, name='tc_page'),

]
