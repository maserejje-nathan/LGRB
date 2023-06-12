from django.db.models import Q
from new.models import *
from payments.models import *

import requests
import json
from datetime import datetime
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from lgrb_els.celery import app

import random
import threading
import datetime
import string
import pytz



def generate_token():
    headers = {'Authorization': 'Basic bDNxTkFGRVphQVg2Nkg1aEE4ZjA3REpreFNBYTpqUGZIZ2FxZ2trUjd3ZmtRWlRpTUU5MzB5NUlh', }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post('https://api-uat.integration.go.ug/token', headers=headers, data=data, verify=False).json()
    return response['access_token']


def check_clearance_status(prn):
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/checkPRNStatus"
    payload = json.dumps({
        "CheckPRNStatus": {
            "strPRN": prn,
            "concatenatedUsernamePasswordSignature": "p8J36tqC5RLtgCMhrClRh6mPOh0xsfgw4gPCl2i9zi4QXVWALc2eUw2uLtJpiZ+pQIXIWjy8IxlaEwITeitajVhelNYCIR2H+DOxPO8WefPTmiY/jICjWqKRg/Q+8ysV1V+kNNifjtu2+zmV17gk12CGL/+/aAWQVjuDZRu4re/Sgl94/FF/Zdi5tDLFZTLFEYuTQghZ//7G7LGttivxNa0fgHmIO12iY0mGfXw6g7et/yPDzpliU7e8vIiSJvxynYUnaBRjzlQw6cXu9oPGAMtR1QHz1NANNwCJPXImWy2/sBgbuvvAjI0cy7zTPfOjxsEwE01T+GDuUVFcax3tDw==",
            "encryptedConcatenatedUsernamePassword": "lRcH7YbF9UTO8vAr9MQm+yANBCOV2zTkpyxJ3176ApIgJraQJqOR5VdjGAYo0HbZpvOBnJ86JQQZbJH1Y6r+4DEBv2T7JwmOpRBqz9aDtO7bj7Pzi+a4R6B57yIyS02FZhQSw0VlcXIoNk10u5RvJgzLv3EmrTfQiU5ExZT+ca2PlRW8psQwZK3VikXtrIUEjCJ0EUHiqDmuV3PSQ4crktF2HawLzEdQVIvJ1Q6MLm5ngh+xRMb42avK2MUM3kd6R2EM64frI4z3RKO/BLY5F6vqJOcfEvmIQEIZm/OkE6xJitaMS9cmf4drW9LlByY3ooyNgVuGF0RY6mVdjqa1qw==",
            "userName": "NITAU"
        }
    })

    token = str(generate_token())
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Cookie': 'ASP.NET_SessionId=rnzjf30gk2nwkl4hdexfy0m5'
    }
    response = requests.post(url, headers=headers, data=payload).json()

    return response


def check_licence_fee_clearance_status(licence_fee_prn):
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/checkPRNStatus"
    payload = json.dumps({
        "CheckPRNStatus": {
            "strPRN": licence_fee_prn,
            "concatenatedUsernamePasswordSignature": "p8J36tqC5RLtgCMhrClRh6mPOh0xsfgw4gPCl2i9zi4QXVWALc2eUw2uLtJpiZ+pQIXIWjy8IxlaEwITeitajVhelNYCIR2H+DOxPO8WefPTmiY/jICjWqKRg/Q+8ysV1V+kNNifjtu2+zmV17gk12CGL/+/aAWQVjuDZRu4re/Sgl94/FF/Zdi5tDLFZTLFEYuTQghZ//7G7LGttivxNa0fgHmIO12iY0mGfXw6g7et/yPDzpliU7e8vIiSJvxynYUnaBRjzlQw6cXu9oPGAMtR1QHz1NANNwCJPXImWy2/sBgbuvvAjI0cy7zTPfOjxsEwE01T+GDuUVFcax3tDw==",
            "encryptedConcatenatedUsernamePassword": "lRcH7YbF9UTO8vAr9MQm+yANBCOV2zTkpyxJ3176ApIgJraQJqOR5VdjGAYo0HbZpvOBnJ86JQQZbJH1Y6r+4DEBv2T7JwmOpRBqz9aDtO7bj7Pzi+a4R6B57yIyS02FZhQSw0VlcXIoNk10u5RvJgzLv3EmrTfQiU5ExZT+ca2PlRW8psQwZK3VikXtrIUEjCJ0EUHiqDmuV3PSQ4crktF2HawLzEdQVIvJ1Q6MLm5ngh+xRMb42avK2MUM3kd6R2EM64frI4z3RKO/BLY5F6vqJOcfEvmIQEIZm/OkE6xJitaMS9cmf4drW9LlByY3ooyNgVuGF0RY6mVdjqa1qw==",
            "userName": "NITAU"
        }
    })

    token = str(generate_token())
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Cookie': 'ASP.NET_SessionId=rnzjf30gk2nwkl4hdexfy0m5'
    }
    response = requests.post(url, headers=headers, data=payload).json()

    return response


# tasks 
@app.task
def check_principlelicence_application_fee_status():
    """
    Query the latest 3 records where the payment_status has not been updated
    """
    licenses = ApplicationFeePayments.objects.filter(
        Q(payment_status__isnull=True) | 
        Q(payment_status__iexact='') | 

        Q(payment_description__isnull=True) | 
        Q(payment_description__iexact='') |

        Q(payment_description = "AVAILABLE") |
        Q(payment_description__iexact="AVAILABLE") | 

        Q(payment_description = "EXPIRED") | 
        Q(payment_description__iexact="EXPIRED") |

        Q(payment_status = "{'@nil': 'true'}") | 
        Q(payment_status__iexact = "{'@nil': 'true'}" ) |

        Q( payment_description = "{'@nil': 'true'}" ) |
        Q( payment_description__iexact = "{'@nil': 'true'}")


  ).order_by('-id')


    if licenses:
        for license in licenses:

            response = check_clearance_status(license.prn)              
            # year_applied = license.date_applied.year + 1   
            if 'CheckPRNStatusResult' in response and 'StatusCode' in response['CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
                license.payment_status = response['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResult']['TaxPayerName']
                license.save()  
            else:
               
                license.payment_status = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['TaxPayerName']

                license.save() 


@app.task
def check_principlelicence_licence_fee_status():
    """
    Query the latest 3 records where the payment_status has not been updated
    """
    licenses = LicenceFeePayments.objects.filter(
        Q(payment_status__isnull=True) |
        Q(payment_status__iexact='') |

        Q(payment_description__isnull=True) |
        Q(payment_description__iexact='') | 

        Q(payment_description = "AVAILABLE") |
        Q(payment_description__iexact="AVAILABLE") | 

        Q(payment_description = "EXPIRED") | 
        Q(payment_description__iexact="EXPIRED") |

        Q(payment_status = "{'@nil': 'true'}") | 
        Q(payment_status__iexact = "{'@nil': 'true'}" ) |

        Q( payment_description = "{'@nil': 'true'}" ) |
        Q( payment_description__iexact = "{'@nil': 'true'}")

    )

    if licenses:
        for license in licenses:

            response = check_licence_fee_clearance_status(license.licence_fee_prn)  

            if 'CheckPRNStatusResult' in response and 'StatusCode' in response['CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
                license.payment_status = response['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResult']['TaxPayerName']
                license.save() 
            else:

                license.payment_status = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['TaxPayerName']
            
                license.save()


@app.task
def check_employee_licence_fee_status():
    """
    Query the latest 3 records where the payment_status has not been updated
    """
    licenses = EmployeeLicence.objects.filter(
            Q(payment_status__isnull=True) | 
            Q(payment_status__iexact='') | 

            Q(payment_description__isnull=True) |
            Q(payment_description__iexact='') |

            Q(payment_description = "AVAILABLE") |
            Q(payment_description__iexact="AVAILABLE") | 

            Q(payment_description = "EXPIRED") | 
            Q(payment_description__iexact="EXPIRED") |

            Q(payment_status = "{'@nil': 'true'}") | 
            Q(payment_status__iexact = "{'@nil': 'true'}" ) |

            Q( payment_description = "{'@nil': 'true'}" ) |
            Q( payment_description__iexact = "{'@nil': 'true'}")


        ).order_by('-date_applied')

    if licenses:
        for license in licenses:

            response = check_clearance_status(license.prn) 

            if 'CheckPRNStatusResult' in response and 'StatusCode' in response['CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
                license.payment_status = response['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResult']['TaxPayerName']
                license.save()  
            else:
                license.payment_status = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['TaxPayerName']
                license.save() 


@app.task
def check_premise_licence_fee_status():
    """
    Query the latest 3 records where the payment_status has not been updated
    """
    licenses = PremiseLicence.objects.filter(
            Q(payment_status__isnull=True) | 
            Q(payment_status__iexact='') | 

            Q(payment_description__isnull=True) |
            Q(payment_description__iexact='') |

            Q(payment_description = "AVAILABLE") |
            Q(payment_description__iexact="AVAILABLE") | 

            Q(payment_description = "EXPIRED") | 
            Q(payment_description__iexact="EXPIRED") |

            Q(payment_status = "{'@nil': 'true'}") | 
            Q(payment_status__iexact = "{'@nil': 'true'}" ) |

            Q( payment_description = "{'@nil': 'true'}" ) |
            Q( payment_description__iexact = "{'@nil': 'true'}")


        ).order_by('-date_applied')

    if licenses:
        for license in licenses:

            response = check_clearance_status(license.prn) 

            if 'CheckPRNStatusResult' in response and 'StatusCode' in response['CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
                license.payment_status = response['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResult']['TaxPayerName']
                license.save()  
            else:
                license.payment_status = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusDesc']
                license.payment_made_on = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['DatePaid']
                license.payment_made_by = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['TaxPayerName']
                license.save() 



# @app.task
# def check_premise_licence_fee_status():
#     """
#     Query the latest 3 records where the payment_status has not been updated
#     """
#     print("started service")
#     licenses = PremisePayment.objects.filter(
#         Q(payment_status__isnull=True) | 
#         Q(payment_status__iexact='') | 

#         Q(payment_description__isnull=True) |
#         Q(payment_description__iexact='') | 

#         Q(payment_description="AVAILABLE") | 
#         Q(payment_description="EXPIRED") |

#         Q(payment_status = "{'@nil': 'true'}") | 
#         Q(payment_status__iexact = "{'@nil': 'true'}" ) |

#         Q( payment_description = "{'@nil': 'true'}" ) |
#         Q( payment_description__iexact = "{'@nil': 'true'}")

#     ).order_by('-date_applied')

#     if licenses:
#         for license in licenses:

#             response = check_clearance_status(license.prn) 

#             if 'CheckPRNStatusResult' in response and 'StatusCode' in response['CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
#                 license.payment_status = response['CheckPRNStatusResult']['StatusCode']
#                 license.payment_description = response['CheckPRNStatusResult']['StatusDesc']
#                 license.payment_made_on = response['CheckPRNStatusResult']['DatePaid']
#                 license.payment_made_by = response['CheckPRNStatusResult']['TaxPayerName']
#                 license.save()  
#             else:

#                 license.payment_status = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusCode']
#                 license.payment_description = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusDesc']
#                 license.payment_made_on = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['DatePaid']
#                 license.payment_made_by = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['TaxPayerName']
            
#                 license.save()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    
    sender.add_periodic_task(2.0, check_principlelicence_application_fee_status.s(
    ), name='principle  application fee status')

    sender.add_periodic_task(2.0, check_principlelicence_licence_fee_status.s(
    ), name='principle licencing  fee status')

    sender.add_periodic_task(
        2.0, check_employee_licence_fee_status.s(), name='employee licence fee status')
    sender.add_periodic_task(
        2.0, check_premise_licence_fee_status.s(), name='premise licence  fee status')
    
   
    
    #  sender.crontab()
    # use crontabs to display the values of the records 

# app.conf.beat_schedule = {
#     "application-fee-status-task": {
#         "task": "check_principlelicence_application_fee_status",
#         "schedule": crontab(minute="*/7")
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
#     }
# }


    


