from  __future__  import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from payments.tasks import *

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lgrb_els.settings')

app = Celery('lgrb_els')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# disable UTC so that Celery can use local time
app.conf.enable_utc = False


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')




# app.conf.beat_schedule = {
#     "application-fee-status-task": {
#         "task": "check_principlelicence_application_fee_status",
#         "schedule": crontab(hour=7, minute=0)
#     },
#     "licence-fee-status-task": {
#         "task": "check_principlelicence_licence_fee_status",
#         "schedule": crontab(minute="*/1")
#     },
#     "employee-licence-fee-status-task": {
#         "task": "check_employee_licence_fee_status",
#         "schedule": crontab(minute="*/1")
#     },
#     "premise-licence-fee-status-task": {
#         "task": "check_premise_licence_fee_status",
#         "schedule": crontab(minute="*/1")
#     },

    
# }

# 2230000106600 paid 
# 2230000106698 not paid

# premise 
# 2230000106699 not paid 