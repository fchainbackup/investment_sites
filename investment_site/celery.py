from __future__ import absolute_import, unicode_literals
import os


from celery import Celery
from django.conf import settings
#from celery.schedule import crontab
from celery import shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment_site.settings')

app = Celery('investment_site')
app.conf.enable_utc = True



app.config_from_object(settings, namespace='CELERY')



app.autodiscover_tasks()

@shared_task
def debug_task(a,b):
    from deposite.models import Deposite
    all_deposite = Deposite.objects.all()
    for dep in all_deposite:
        if dep.transaction_mode == "approved" and dep.trade_mode == "running":
            try:
                time= int(dep.time_of_trade)
                seconds = time * 60 * 60
                total_cycle = seconds/60
                profit=(dep.ammount/100) * dep.profit_percent
                profit_per_record = profit/total_cycle
                dep.profit += profit_per_record
                dep.time_count_for_trade += 60
                dep.save()
            except:
                dep.time_count_for_trade += 60
                dep.save()
    return "done"
    



#>celery -A investment_site beat -l INFO
#celery -A investment_site.celery worker -l info --pool=solo