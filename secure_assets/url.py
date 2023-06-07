from django.urls import path
from .views import secure_asset_detail_page,secure_asset,secure_asset_json



app_name = "secure_assets"

urlpatterns = [
    path('', secure_asset_detail_page,name="secure_asset"),
    path('user/', secure_asset,name="secure_asset_user"),
    path('check_secure/', secure_asset_json,name="if_secured")
]
