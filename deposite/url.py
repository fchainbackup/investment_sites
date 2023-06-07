from django.urls import path
from .views import deposite,complete_deposite_transaction,my_investment,my_transaction,save_prof



app_name = "deposite"

urlpatterns = [
    path('',deposite,name="deposite-page" ),
    path('complete_transaction/',complete_deposite_transaction,name="complete-deposite" ),
    path('my_investments/',my_investment,name="my_investment-page" ),
    path('my_transactions/',my_transaction,name="my_transaction-page" ),
    path('my_investments/save_prof/',save_prof,name="save_prof-ajax" ),
    
]
