from multiprocessing import context
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import  View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.http.response import JsonResponse

from django.db.models import Q
from account.decorators import *
from new.forms import *
from payments.models import *
from payments.forms import *

# pdf stuff
from django.contrib.staticfiles import finders
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
from payments.forms import  *


def ura_token(request):
    
    headers = { 
        'Authorization': 'Basic bDNxTkFGRVphQVg2Nkg1aEE4ZjA3REpreFNBYTpqUGZIZ2FxZ2trUjd3ZmtRWlRpTUU5MzB5NUlh',
        #  'Authorization': 'Basic bDNxTkFGRVphQVg2Nkg1aEE4ZjA3REpreFNBYTpqUGZIZ2FxZ2trUjd3ZmtRWlRpTUU5MzB5NUlh',

    }
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://api-uat.integration.go.ug/token', headers=headers, data=data, verify=False).json()
    token = response['access_token']

    print(response)
    # return HttpResponse(token)
    
    return token
 

def verify_tin(request):
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/getClientRegistration"
    tin = request.POST.get('tin') 
    # 1000035867
    payload = json.dumps({
        "GetClientRegistration": {
            "TIN": tin,
            "concatenatedUsernamePasswordSignature": "OZH2QDH8l++IU63ZT6Sz6T1lubBsBEwyAXflY0z9HNK/R8Bj//ozcOYjRv5oRty60XIDUY+an8tLm7fkJxT4hDx35icdTXlLhoR8XiXZwgMUHmrgz/0VBsxRXl+Fhp3javLn6ReIcanfXnIkcLGE5rC/NTB83wBxWpcXuH+Q8rOvJzJ6QHOwAD1e7AVPFyambQTr3gpdUiEC3nfaN4XcXvJ1bq/SgMkkCjzkB3mRJOUdHZnaqu/zx8+5M9EW1Qlj2UnN5qLHVT0q/q7RdDZMnGyN1erMm9LpvFRIg9cBXBcUc4m0ZJo3Q5H6JL4jqnOw5tmN3jTr4oUs4wiOQloy4g==",
            "encryptedConcatenatedUsernamePassword": "HKiFwkIeXzAQ0vDCsRwUMmFipkCTOHuU/ll9/3M7SRJ7l8jMpCZBjQkew6iZvq6paAQCwLZNbzPKeB1oWh3jlKLBzJA5IB0Y1cmmnCOEUL+siDdI1/GMyD/MUXkQJ5jTqDLrAqhimDgWa1fvmvmSL2+x+cyV1LLo4tN6JlKEau3rC0LnMOy1LBdkUmHLHsA7Vcgj2DnD/BxRMIh7Lcl5QsQUFzSRxTkjxNwyjR8KiUFTtX1wyGRoolBVWZ/+4BISWwoPHppUcIkXHqNvBQVkAY8gQGzdCrZ+zKIZXhAGx5E0F7/QR7VQ9oK2Ezvc2B2UUFgMjCADRNJ62KXgMcsnpQ==",
            "userName": "NITAU"
        }
    })

    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {str(ura_token(request))}',
        'Content-Type': 'application/json',
        'Cookie': 'ASP.NET_SessionId=rnzjf30gk2nwkl4hdexfy0m5'
    }

    response = requests.post(url, headers=headers, data=payload).json()
    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


# application fee 
def get_prn_application_fee(request, *args, **kwargs):
    #  application fees LGRB002
    # licence fees LGRB001
    # KCCA524 kcca 
    
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/getPRN"

    application_fee = request.POST.get('application_fee') 

    tin = request.POST.get('tin') 
    
    payload = json.dumps({
        "PRNRequest": {
            "AdditionalFees": "0",
            "Amount": application_fee, # "160250"
            "AssessmentDate": "2021-04-04T12:16:15.534",
            "BuildingName": None,
            "ContactNo": None,
            "County": None,
            "District": None,
            "Email": "kk19700@hotmail.com", # Email,
            "ExpiryDays": "21", 
            "ForeignCurrencyCode": None,
            "GrossAmount": "0",
            "LocalCouncil": None,
            "MobileNo": "256750355555", # MobileNo
            "NoOfForms": "1",
            "Parish": None,
            "PaymentBankCode": "DTB",
            "PaymentMode": "CASH",
            "PaymentType": "DT",
            "PlotNo": None,
            "ReferenceNo": "0001069329",
            "SRCSystem": "eCitie",
            "Street": None,
            "SubCounty": None,
            "TIN": tin, # "1000035867"
            "TaxHead": "LGRB002",
            "TaxPayerBankCode": "DTB",
            "TaxPayerName": "ALIFAT INVESTMENTS LTD", # TaxPayerName
            "TaxSubHead": None,
            "TraceCentre": None,
            "Village": None
        },

    #  kcca cred
    # "concatenatedUsernamePasswordSignature": "husLqkBMuZlu657ng+CIXXG2HWJN1gvtRm5Qx+mILbzeAg4kqKO+s0WIBtNgIXBP7FDrthzUC0FKhjXygNmuvoYbCcbQpTLRvs2CayYl5gjcNtgnAvErX7jdV2gWhMntbfD1Os0S+rYRqfXMka3peDYZ5KAq4ZaN1ArZRhH8AI73KYC3AZtk4lTLijL9tH7TNjP/L4qeo9gVC9Mjmk4ZROcmVrVffDk4yDw7VPUBThI7ED83YvNhEKbPAaUH04uP9m0VvILhxEK1mlkBgjplmgy3Itw95AVq3H7802AKBs8KQNl9qHIr2vXGmj1jI7nbkCVb1vz+KQEBYjGEfRhgFg==",
    # "encryptedConcatenatedUsernamePassword": "FZJ9kV8kzTXApRMj5KhaEd7pc/S1ma3x5OMOFMChpdazAoGz4bBCED7AYNdUmBiL9cIPhq+bY4mkbVEHvzNHg0ek4eNQ/w8E60ovBoIvrj8uVFEn2V0RCDDa5ipmi0rjM8Rm2jvLrNYzkFNVb7SVT+lQj5NyRR9X/1mXSYUYhpW8G6GdE9yUOVrX48wqMSOV3QlBbrjHTtl4X7CMqXQ6+zXUVPjKwZtoDt5XRoHFxHTbV0hxgil0fVG4i+VT3LQN5Jt8jC3QJdc8bp8Ib5bmOWHsmKXiH4A0ZjbYFsiUkNcDmU7+MDgcjX7urbtJWBdJhTUHyFsdF1LBztAsXWuXxQ==",
    # "userName": "NITAU"

    # creds 2
    "encryptedConcatenatedUsernamePassword": "Kb4WRvAz6q6y3fJvX7bMuF8DEpfvDA4pukolLsEbzSO5A6EYrDXn+HpjfMZmsw3IJT/jvuduwYMSz2vGZ7zHFVmqvTi2GsRdbDvXx0ObxDDoSTSexzr7JblFX2IMrkOCLQZaxwHSiAV3Aqlz++tj9O0/8IPKG+DzdD7CNY25WMaveVDN5IXqZaerWJ0lmLMeFWsPf7EtfHsbZ1qmz2ZDh1viuoSomkUVEw0PHcChtEVfF2Jdo6Ji69ukYWYnlcqFlVj8OyWEiepYlFd6KZ9NGR7GfIwyi/MUZCzHW7mADoRXhkHvdOuKp4j8MPqB6BEVLWkh+sgjYV2PIPmkw7KVuQ==",
    "concatenatedUsernamePasswordSignature": "EIZjeAoaXtmSe8H8H49QqezfZttE3l2Xux3SNW32Ta8Wz1adlDK1SlIAs5X6FQvyGS6Dig+rnWBF3bJtlqnYpOMAmZ1A6r26qYiFbA8Dnq7Hj7J5aIAoMveO8ymhBGJQx9+cjjtXfsDEo5Tcm9zJd3UBmccTROD98oDRGIQqmJAjPl/r/UNr96Rq8/HNcYockw4x4Y4y3voMnKWjFyFjgBHI5zYGTqi+OUNAtIpBo42etJxqBHiWjrL2HgXrzqkgQH4MZmvBE4tvPZSJs6zh/U7npWswA1k/6bxHMUqEwxUtQxhuCGll1kZLHmaJ4weOr/xgjHuoyhtHuiS7ANmfyQ==",
    "userName": "LGRB"

    # creds 1
    # "encryptedConcatenatedUsernamePassword": "jIPo6bJQxUAICJQuJ8IMB0ugd4IDnWr+NoVek3eU2N3WFR06AA0ubYYcxelXG+2nnkZ3tn9qcBJdyZGetRWYeM1kzYrN7iLTnsuQdbmYVo+GyaNVPwT+Aov4Rlfaytd8N8m28DdpxjF7WF+WWI9on4ozZjI5unXK6QvYTMGPqS3tx/Qj3l9or8Jd82Kfmr8oAxXjuEh+DuSCNmehAYp4OnwpWix6RCDuGf4E+Op0ltzTFdYVOH9DVxjFX7B/AUoenGYd4IF8dkTMkmH4/3iFZyEaFMx79bfbkkz3bofJsJ7Y0Nz4lMnz/e65PKhC03akAfd7s341k+RyPXhV2DgitA==",   
    # "concatenatedUsernamePasswordSignature": "vUaPn2UUa51JNy8WdcIrYpPo3iTZClsL2H4u7Mgu9ldukOU9N8PImvytJtkqEq3ormSHaszT/H/1fNG60XycYSjt8l6e2WR8L3j8qf4DLLFzin6nHUiJST94BNSF0f/Br/nAraJRZCaRSlZR+bbdIvaLnB7iHZT7zRPs/wnuK6QhXu7e88Csx2oD7cM1q2enoD+uJwV/mYUhbqvwN7qureQfnYWV8FCOPNoxzP1tOWTiXPBz320kDtpa7DgRIBcNXptBaB7GkCLOLsvYqaFmVRX5xekkLqRDV3ZnTIifEinQ+HD+NvWVNDXo3I7Rw0kFcU0tj7oEO97ykP/GigJFrg==",
    # "userName": "LGRB"

    })
        
        
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {str(ura_token(request))}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload).json()

    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


# licence fee payment 
def get_prn_licence_fee(request, *args, **kwargs):
    
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/getPRN"
    licence_fee = request.POST.get('licence_fee') 
    tin = request.POST.get('licence_fee_tin') 
    
    payload = json.dumps({
        "PRNRequest": {
            "AdditionalFees": "0",
            "Amount": licence_fee, # "160250"
            "AssessmentDate": "2021-04-04T12:16:15.534",
            "BuildingName": None,
            "ContactNo": None,
            "County": None,
            "District": None,
            "Email": "kk19700@hotmail.com", # Email,
            "ExpiryDays": "21", 
            "ForeignCurrencyCode": None,
            "GrossAmount": "0",
            "LocalCouncil": None,
            "MobileNo": "256750355555", # MobileNo
            "NoOfForms": "1",
            "Parish": None,
            "PaymentBankCode": "DTB",
            "PaymentMode": "CASH",
            "PaymentType": "DT",
            "PlotNo": None,
            "ReferenceNo": "0001069329",
            "SRCSystem": "eCitie",
            "Street": None,
            "SubCounty": None,
            "TIN": tin, # "1000035867"
            "TaxHead": "LGRB001",
            "TaxPayerBankCode": "DTB",
            "TaxPayerName": "ALIFAT INVESTMENTS LTD", # TaxPayerName
            "TaxSubHead": None,
            "TraceCentre": None,
            "Village": None
        },
    
        "encryptedConcatenatedUsernamePassword": "Kb4WRvAz6q6y3fJvX7bMuF8DEpfvDA4pukolLsEbzSO5A6EYrDXn+HpjfMZmsw3IJT/jvuduwYMSz2vGZ7zHFVmqvTi2GsRdbDvXx0ObxDDoSTSexzr7JblFX2IMrkOCLQZaxwHSiAV3Aqlz++tj9O0/8IPKG+DzdD7CNY25WMaveVDN5IXqZaerWJ0lmLMeFWsPf7EtfHsbZ1qmz2ZDh1viuoSomkUVEw0PHcChtEVfF2Jdo6Ji69ukYWYnlcqFlVj8OyWEiepYlFd6KZ9NGR7GfIwyi/MUZCzHW7mADoRXhkHvdOuKp4j8MPqB6BEVLWkh+sgjYV2PIPmkw7KVuQ==",
        "concatenatedUsernamePasswordSignature": "EIZjeAoaXtmSe8H8H49QqezfZttE3l2Xux3SNW32Ta8Wz1adlDK1SlIAs5X6FQvyGS6Dig+rnWBF3bJtlqnYpOMAmZ1A6r26qYiFbA8Dnq7Hj7J5aIAoMveO8ymhBGJQx9+cjjtXfsDEo5Tcm9zJd3UBmccTROD98oDRGIQqmJAjPl/r/UNr96Rq8/HNcYockw4x4Y4y3voMnKWjFyFjgBHI5zYGTqi+OUNAtIpBo42etJxqBHiWjrL2HgXrzqkgQH4MZmvBE4tvPZSJs6zh/U7npWswA1k/6bxHMUqEwxUtQxhuCGll1kZLHmaJ4weOr/xgjHuoyhtHuiS7ANmfyQ==",
        "userName": "LGRB"
    })
    
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {str(ura_token(request))}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload).json()
    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


# inspection fee 
def get_prn_inspection_fee(request, *args, **kwargs):
    #  application fees LGRB002
    # licence fees LGRB001
    # KCCA524 kcca 
    
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/getPRN"

    inspection_fee = request.POST.get('inspection_fee') 

    tin = request.POST.get('tin') 
    
    payload = json.dumps({
        "PRNRequest": {
            "AdditionalFees": "0",
            "Amount": inspection_fee, # "160250"
            "AssessmentDate": "2021-04-04T12:16:15.534",
            "BuildingName": None,
            "ContactNo": None,
            "County": None,
            "District": None,
            "Email": "kk19700@hotmail.com", # Email,
            "ExpiryDays": "21", 
            "ForeignCurrencyCode": None,
            "GrossAmount": "0",
            "LocalCouncil": None,
            "MobileNo": "256750355555", # MobileNo
            "NoOfForms": "1",
            "Parish": None,
            "PaymentBankCode": "DTB",
            "PaymentMode": "CASH",
            "PaymentType": "DT",
            "PlotNo": None,
            "ReferenceNo": "0001069329",
            "SRCSystem": "eCitie",
            "Street": None,
            "SubCounty": None,
            "TIN": tin, # "1000035867"
            "TaxHead": "LGRB002",
            "TaxPayerBankCode": "DTB",
            "TaxPayerName": "ALIFAT INVESTMENTS LTD", # TaxPayerName
            "TaxSubHead": None,
            "TraceCentre": None,
            "Village": None
        },

    #  kcca cred
    # "concatenatedUsernamePasswordSignature": "husLqkBMuZlu657ng+CIXXG2HWJN1gvtRm5Qx+mILbzeAg4kqKO+s0WIBtNgIXBP7FDrthzUC0FKhjXygNmuvoYbCcbQpTLRvs2CayYl5gjcNtgnAvErX7jdV2gWhMntbfD1Os0S+rYRqfXMka3peDYZ5KAq4ZaN1ArZRhH8AI73KYC3AZtk4lTLijL9tH7TNjP/L4qeo9gVC9Mjmk4ZROcmVrVffDk4yDw7VPUBThI7ED83YvNhEKbPAaUH04uP9m0VvILhxEK1mlkBgjplmgy3Itw95AVq3H7802AKBs8KQNl9qHIr2vXGmj1jI7nbkCVb1vz+KQEBYjGEfRhgFg==",
    # "encryptedConcatenatedUsernamePassword": "FZJ9kV8kzTXApRMj5KhaEd7pc/S1ma3x5OMOFMChpdazAoGz4bBCED7AYNdUmBiL9cIPhq+bY4mkbVEHvzNHg0ek4eNQ/w8E60ovBoIvrj8uVFEn2V0RCDDa5ipmi0rjM8Rm2jvLrNYzkFNVb7SVT+lQj5NyRR9X/1mXSYUYhpW8G6GdE9yUOVrX48wqMSOV3QlBbrjHTtl4X7CMqXQ6+zXUVPjKwZtoDt5XRoHFxHTbV0hxgil0fVG4i+VT3LQN5Jt8jC3QJdc8bp8Ib5bmOWHsmKXiH4A0ZjbYFsiUkNcDmU7+MDgcjX7urbtJWBdJhTUHyFsdF1LBztAsXWuXxQ==",
    # "userName": "NITAU"

    # creds 2
    "encryptedConcatenatedUsernamePassword": "Kb4WRvAz6q6y3fJvX7bMuF8DEpfvDA4pukolLsEbzSO5A6EYrDXn+HpjfMZmsw3IJT/jvuduwYMSz2vGZ7zHFVmqvTi2GsRdbDvXx0ObxDDoSTSexzr7JblFX2IMrkOCLQZaxwHSiAV3Aqlz++tj9O0/8IPKG+DzdD7CNY25WMaveVDN5IXqZaerWJ0lmLMeFWsPf7EtfHsbZ1qmz2ZDh1viuoSomkUVEw0PHcChtEVfF2Jdo6Ji69ukYWYnlcqFlVj8OyWEiepYlFd6KZ9NGR7GfIwyi/MUZCzHW7mADoRXhkHvdOuKp4j8MPqB6BEVLWkh+sgjYV2PIPmkw7KVuQ==",
    "concatenatedUsernamePasswordSignature": "EIZjeAoaXtmSe8H8H49QqezfZttE3l2Xux3SNW32Ta8Wz1adlDK1SlIAs5X6FQvyGS6Dig+rnWBF3bJtlqnYpOMAmZ1A6r26qYiFbA8Dnq7Hj7J5aIAoMveO8ymhBGJQx9+cjjtXfsDEo5Tcm9zJd3UBmccTROD98oDRGIQqmJAjPl/r/UNr96Rq8/HNcYockw4x4Y4y3voMnKWjFyFjgBHI5zYGTqi+OUNAtIpBo42etJxqBHiWjrL2HgXrzqkgQH4MZmvBE4tvPZSJs6zh/U7npWswA1k/6bxHMUqEwxUtQxhuCGll1kZLHmaJ4weOr/xgjHuoyhtHuiS7ANmfyQ==",
    "userName": "LGRB"

    # creds 1
    # "encryptedConcatenatedUsernamePassword": "jIPo6bJQxUAICJQuJ8IMB0ugd4IDnWr+NoVek3eU2N3WFR06AA0ubYYcxelXG+2nnkZ3tn9qcBJdyZGetRWYeM1kzYrN7iLTnsuQdbmYVo+GyaNVPwT+Aov4Rlfaytd8N8m28DdpxjF7WF+WWI9on4ozZjI5unXK6QvYTMGPqS3tx/Qj3l9or8Jd82Kfmr8oAxXjuEh+DuSCNmehAYp4OnwpWix6RCDuGf4E+Op0ltzTFdYVOH9DVxjFX7B/AUoenGYd4IF8dkTMkmH4/3iFZyEaFMx79bfbkkz3bofJsJ7Y0Nz4lMnz/e65PKhC03akAfd7s341k+RyPXhV2DgitA==",   
    # "concatenatedUsernamePasswordSignature": "vUaPn2UUa51JNy8WdcIrYpPo3iTZClsL2H4u7Mgu9ldukOU9N8PImvytJtkqEq3ormSHaszT/H/1fNG60XycYSjt8l6e2WR8L3j8qf4DLLFzin6nHUiJST94BNSF0f/Br/nAraJRZCaRSlZR+bbdIvaLnB7iHZT7zRPs/wnuK6QhXu7e88Csx2oD7cM1q2enoD+uJwV/mYUhbqvwN7qureQfnYWV8FCOPNoxzP1tOWTiXPBz320kDtpa7DgRIBcNXptBaB7GkCLOLsvYqaFmVRX5xekkLqRDV3ZnTIifEinQ+HD+NvWVNDXo3I7Rw0kFcU0tj7oEO97ykP/GigJFrg==",
    # "userName": "LGRB"

    })
        
        
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {str(ura_token(request))}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload).json()

    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')



def get_new_bank_guarantee_data(request):
   
    if request.method == "POST":
        certificate_number = request.POST['certificate_number']
       
        approved_licence = PrincipleLicence.objects.filter(
            certificate_number=certificate_number, 
            approved=True
        )
        
        if approved_licence:
            for licence in approved_licence:

                email = licence.email
                name_of_the_company = licence.name_of_the_company
                
                message = {
                    "code": 200,
                    "message": "success",
                    "email": email,
                    "name_of_the_company": name_of_the_company
                }

                print(message)
                return JsonResponse({'data':message})

        else:
            print("not found ")
            return HttpResponse("not found ")
   

def checkClearanceStatus(request):
    print("inside method")
    
    # Prn = str(request.POST.get('Prn'))
    # Prn = f"\"{request.POST.get('Prn')}\""
    Prn = request.POST.get('Prn')
    # url = f"https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/checkPRNStatus?strPRN={Prn}"
    url = "https://api-uat.integration.go.ug/t/ura.go.ug/ura-mdapayment-api/1.0.0/checkPRNStatus"

    print(Prn)
    #  2220000008739
    payload = json.dumps({
        "CheckPRNStatus": {
            "strPRN": Prn,
            "encryptedConcatenatedUsernamePassword": "Kb4WRvAz6q6y3fJvX7bMuF8DEpfvDA4pukolLsEbzSO5A6EYrDXn+HpjfMZmsw3IJT/jvuduwYMSz2vGZ7zHFVmqvTi2GsRdbDvXx0ObxDDoSTSexzr7JblFX2IMrkOCLQZaxwHSiAV3Aqlz++tj9O0/8IPKG+DzdD7CNY25WMaveVDN5IXqZaerWJ0lmLMeFWsPf7EtfHsbZ1qmz2ZDh1viuoSomkUVEw0PHcChtEVfF2Jdo6Ji69ukYWYnlcqFlVj8OyWEiepYlFd6KZ9NGR7GfIwyi/MUZCzHW7mADoRXhkHvdOuKp4j8MPqB6BEVLWkh+sgjYV2PIPmkw7KVuQ==",
            "concatenatedUsernamePasswordSignature": "EIZjeAoaXtmSe8H8H49QqezfZttE3l2Xux3SNW32Ta8Wz1adlDK1SlIAs5X6FQvyGS6Dig+rnWBF3bJtlqnYpOMAmZ1A6r26qYiFbA8Dnq7Hj7J5aIAoMveO8ymhBGJQx9+cjjtXfsDEo5Tcm9zJd3UBmccTROD98oDRGIQqmJAjPl/r/UNr96Rq8/HNcYockw4x4Y4y3voMnKWjFyFjgBHI5zYGTqi+OUNAtIpBo42etJxqBHiWjrL2HgXrzqkgQH4MZmvBE4tvPZSJs6zh/U7npWswA1k/6bxHMUqEwxUtQxhuCGll1kZLHmaJ4weOr/xgjHuoyhtHuiS7ANmfyQ==",
            "userName": "LGRB"
        }
    })
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {str(ura_token(request))}',
        'Content-Type': 'application/json',
        'Cookie': 'ASP.NET_SessionId=rnzjf30gk2nwkl4hdexfy0m5'
    }
    response = requests.post(url, headers=headers, data=payload).json()
    
    return HttpResponse(json.dumps(response), content_type='application/json')


decorators = [login_required(login_url='login'), allowed_users( allowed_roles=[ 'client'])]
@method_decorator(decorators, 'dispatch')
class ApplicationFeePayment(View):
    form_class = ApplicationFeePaymentForm

    def post(self, request):
        # Retrieve the raw JSON data from the request body
        data = json.loads(request.body)

        form = self.form_class(data)
        if form.is_valid():
            application_fee_form = form.save(commit=False)
            licence_id = data.get('licence_id')
            print(licence_id)
            try:
                licence = PrincipleLicence.objects.get(id=licence_id)
            except PrincipleLicence.DoesNotExist:
                return JsonResponse({'success': False, 'errors': 'Licence not found'})
            
            application_fee_form.save()
            
            licence.applicationfeepayments = application_fee_form
            
            licence.save()
            
            return JsonResponse({'success': True, 'message': 'Payment added successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


decorators = [login_required(login_url='login'), allowed_users( allowed_roles=['verifier', 'approver', 'inspector', 'admin_officer', 'client'])]
@method_decorator(decorators, 'dispatch')
class LicenceFeePayment(View):

    form_class = LicenceFeePaymentForm

    def post(self, request):
        # Retrieve the raw JSON data from the request body
        data = json.loads(request.body)

        form = self.form_class(data)

        if form.is_valid():
            licence_fee_form = form.save(commit=False)
            licence_id = data.get('licence_id')
            print(licence_id)
            try:
                licence = PrincipleLicence.objects.get(id=licence_id)
            except PrincipleLicence.DoesNotExist:
                return JsonResponse({'success': False, 'errors': 'Licence not found'})
            
            licence_fee_form.save()
            
            licence.licencefeepayments = licence_fee_form
            
            licence.save()
            
            return JsonResponse({'success': True, 'message': 'PRN for licence fee generated successfully'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})


decorators = [login_required(login_url='login'), allowed_users( allowed_roles=['verifier', 'approver', 'inspector', 'admin_officer', 'client'])]
@method_decorator(decorators, 'dispatch')
class LicenceFeePayments(View):

    template_name = 'payments/principle_licence_payment.html'
    form_class = LicenceFeePaymentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form_class = LicenceFeePaymentForm(request.POST, request.FILES)
        form = form_class
        
        if form.is_valid():
            license_fee_payment = form.save(commit=False)
            certificate_no = form.cleaned_data.get('principle_licence_certificate_number')
            license_fee_payment.save()
            if license_fee_payment:
                principle_license = PrincipleLicence.objects.filter(Q(certificate_number=certificate_no)).first()
                if principle_license:
                    principle_license.principle_licence_paymentid = license_fee_payment
                    principle_license.save()
                    messages.success(request, 'PRN has been generated successfully')
            
                    return redirect('client:client_home')

                
        return render(request, self.template_name, {'form': form})


class ListPremisesPayments(View):
    template_name = 'payments/premise_payment_list.html'

    def get(self, request):
        context = {}
        context['new_licence_premise_payments'] = PremisePayment.objects.all(
            # email = request.user.email
        )

        return render(request, self.template_name, context) 


class ClientPremisesPaymentsList(View):
    template_name = 'payments/client_premise_payment_list.html'

    def get(self, request):
        
        context = {}

        context['clients_premise_payment_records'] = PremisePayment.objects.filter(
            email = request.user.email
        )

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'), allowed_users( allowed_roles=['verifier', 'approver', 'inspector', 'admin_officer', 'client'])]
@method_decorator(decorators, 'dispatch')
class PremisesPayment(View):

    template_name = 'payments/create_premise_payment.html'
    form_class = PremiseLicencePaymentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form_class = PremiseLicencePaymentForm(request.POST, request.FILES)
        form = form_class
        
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, 'Premise payment added successfully ')
                
        return render(request, self.template_name, {'form': form})
    

def premise_pdf_download(request, *args, **kwargs):
    pk = kwargs.get('pk')
    # certificate = get_object_or_404(PremiseLicence, pk=pk )
    premises = PremiseLicence.objects.filter(email=request.user.email)
    template_path = 'new/certificate/premises_pdf_list.html'
    context = {
        'premises': premises
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF( html, dest=response )
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
