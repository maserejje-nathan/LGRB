from functools import reduce
from operator import and_
import os
import time
import json
import io
from pathlib import Path
import xmltodict
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages


from django import template

from .decorators import *
from account.forms import *
from account.models import Account
from account.intergrations import URLS, SCOPES, PRIVATE_KEY

__author__ = 'bdm4'

import requests, json
import subprocess
import jwt
# from jwt import PyJWKClient
import datetime
import secrets

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from account.intergrations import URLS, SCOPES, PRIVATE_KEY
from account.intergrations import URLS, SCOPES, PRIVATE_KEY

def auth_page(request):
    return render(request, 'account/auth.html')


def client_login(request):
    context = {}
    user = request.user
    if user.is_authenticated:

        landing_page = 'client:client_home'

        if user.role == "client":
            landing_page = 'client:client_home'
        elif user.role == "inspector":
            landing_page = 'administrator:inspecting_officer_home'
        elif user.role == "verifier":
            landing_page = 'administrator:verification_officer_home'
        elif user.role == "approver":
            landing_page = 'administrator:approving_officer_home'
        elif user.role == "admin":
            landing_page = 'administrator:admin_home'

        return redirect(landing_page)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)

                landing_page = 'client:client_home'

                if user.role == "client":
                    landing_page = 'client:client_home'
                elif user.role == "inspector":
                    landing_page = 'administrator:inspecting_officer_home'
                elif user.role == "verifier":
                    landing_page = 'administrator:verification_officer_home'
                elif user.role == "approver":
                    landing_page = 'administrator:approving_officer_home'
                elif user.role == "admin":
                    landing_page = 'administrator:admin_home'

                return redirect(landing_page)
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "account/login.html", context)

             
def client_logout(request):
    logout(request)
    return redirect('/')


def admin_login(request):
    context = {}
    user = request.user
    if user.is_authenticated:

        landing_page = 'client:client_home'

        if user.role == "client":
            landing_page = 'client:client_home'
        elif user.role == "inspector":
            landing_page = 'administrator:inspecting_officer_home'
        elif user.role == "verifier":
            landing_page = 'administrator:verification_officer_home'
        elif user.role == "approver":
            landing_page = 'administrator:approving_officer_home'
        elif user.role == "admin":
            landing_page = 'administrator:admin_home'

        return redirect(landing_page)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)

                landing_page = 'client:client_home'

                if user.role == "client":
                    landing_page = 'client:client_home'
                elif user.role == "inspector":
                    landing_page = 'administrator:inspecting_officer_home'
                elif user.role == "verifier":
                    landing_page = 'administrator:verification_officer_home'
                elif user.role == "approver":
                    landing_page = 'administrator:approving_officer_home'
                elif user.role == "admin":
                    landing_page = 'administrator:admin_home'

                return redirect(landing_page)
    else:
        form = AccountAuthenticationForm()
    context['admin_login_form'] = form
    # return render(request, "account/admin_login.html", context)
    return render(request, "account/admin_login_extended.html", context)


def admin_logout(request):
    logout(request)
    return redirect('/login/admin')


class RegisterView(View):

    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):

        context = {}
        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('login')
              
        else:
            
            context['registration_form'] = form
            return render(request, self.template_name, context)


    
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "full_names": request.POST['full_names'],
                "phone_number": request.POST['phone_number'],
                "image": request.POST['image'],
               
                # location stuff 
                "District": request.POST['District'],
                "County": request.POST['County'],
                "Subcounty": request.POST['Subcounty'],
                "Parish": request.POST['Parish'],
                "Village": request.POST['Village'],

            }
            account = form.save(commit=False)
            
            account.full_names = str( form.cleaned_data.get('full_names')).title()
            # location 
            account.District = str(form.cleaned_data.get('District')).title(),
            account.County = str(form.cleaned_data.get('County')).title(),
            account.Subcounty = str(form.cleaned_data.get('Subcounty')).title(),
            account.Parish = str(form.cleaned_data.get('Parish')).title(),
            account.Village = str(form.cleaned_data.get('Village')).title(),

            account.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                "email": request.user.email,
                "phone_number": request.user.phone_number,
                "image": request.user.image,
                #  location 
                "District": request.user.District,
                "County": request.user.County,
                "Subcounty": request.user.Subcounty,
                "Parish": request.user.Parish,
                "Village": request.user.Village
            }
        )

        context['account_form'] = form
    return render(request, "account/profile.html", context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})


def enablejs(request):
    return render(request, 'account/enablejs.html', {})


BASE_DIR = Path(__file__).resolve().parent.parent
temp_email_txt = os.path.join(
    BASE_DIR, 'account\\templates\\account\\password\\pasword_reset_email.txt')
temp_email_html = os.path.join(
    BASE_DIR, 'account\\templates\\account\\password\\pasword_reset_email.html')


def PasswordResetRequestView(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Account.objects.filter(
                Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    plaintext = template.loader.get_template(temp_email_txt)
                    htmltemp = template.loader.get_template(temp_email_html)
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    text_content = plaintext.render(c)
                    html_content = htmltemp.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, 'Website <admin@example.com>', [
                                                     user.email], headers={'Reply-To': 'admin@example.com'})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.info(
                        request, "Password reset instructions have been sent to the email address entered.")
                    return redirect("login")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="account/password_reset.html", context={"password_reset_form": password_reset_form})


def ursb_token(request):
    headers = {  'Authorization': 'Basic d0RrdUxSM2dYUkl2dzdjVjZxZmY3Y2pKVDRVYTpoUzRPS1FacHJRSWVIMHMxQmZwemI2eUVTSFFh',  }
    data = {  'grant_type': 'client_credentials'  }
    response = requests.post('https://api-uat.integration.go.ug/token', headers=headers, data=data, verify=False).json()
    token = response['access_token']
    print(token)
    return token


def nira_token(request):

    # curl -k -X POST https://api-uat.integration.go.ug/token -d "grant_type=client_credentials" -H"Authorization: 
    # Basic ZmtTb2NFcE56WUROWWY1cld4VW45bGxrTVNBYTpwZjlnSWYxVWZIQUZqZEh6VUlkbWlqSGdZSmdh"

    headers = { 'Authorization': 'Basic ZmtTb2NFcE56WUROWWY1cld4VW45bGxrTVNBYTpwZjlnSWYxVWZIQUZqZEh6VUlkbWlqSGdZSmdh'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://api-uat.integration.go.ug/token', headers=headers, data=data, verify=False).json()
    token = response['access_token']
    print(token)
    return token


def update_nira_password():
    # add a celery task to update the password after some days and also hash it 
    # query the db to return hashed password 
    pass 


def nira_credentials_token(request):
    url = "https://api-uat.integration.go.ug/t/nira.go.ug/nitaauth/1.0.0/api/v1/access"
    payload = json.dumps(
        {
            "username": "nita-u@root",
            "password": "Bsd!679"
            
        }
    )

    headers = {
        'Authorization': f'Bearer {str(nira_token(request))}',
        'Content-Type': 'application/json'
    }
  
    response = requests.post( url, headers=headers, data=payload, verify=False ).json()

    datas = json.dumps({
        "nira_auth_forward" : response['NIRA AUTH FORWARD'],
        "nira_nonce" : response['NONCE'],
        "nira_created" : response['CREATED DATE'],
    })
   

    return datas


def nira(request, *args, **kwargs):

    credentials =  json.loads(nira_credentials_token(request))
    nira_auth_forward = credentials['nira_auth_forward']
    nira_nonce = credentials['nira_nonce']  
    nira_created = credentials['nira_created']

    print(nira_auth_forward)
    print(nira_nonce)
    print(nira_created)
   
    headers = {
        'Authorization': f'Bearer {str(nira_token(request))}',
        'nira-auth-forward': f"{str(nira_auth_forward)}",
        'nira-nonce': f"{str(nira_nonce)}",
        'nira-created': f"{str(nira_created)}"
    }

    # implementation 1 -> getPerson information 
    # nin = request.POST.get('nin')
    # url = f"https://api-uat.integration.go.ug/t/nira.go.ug/nira-api/1.0.0/getPerson?nationalId={nin}"
    # response = requests.get(url, headers=headers, verify=False).json()
    # print(response)

    # return HttpResponse(json.dumps(response), content_type='application/json')

    # implementation 2 -> verifyPerson information

    # payload = json.dumps({
    #     "dateOfBirth": "",
    #     "documentId": card_number,
    #     "givenNames": last_name,
    #     "nationalId": nin,
    #     "surname": first_name
    # })

    

    data = json.loads(request.body)
    payload = json.dumps({
        "dateOfBirth": "",
        "documentId": data['card_number'],
        "givenNames": data['first_name'],
        "nationalId": data['nin'],
        "surname": data['last_name']
        })
    print(payload )
    # print(data)

    url = "https://api-uat.integration.go.ug/t/nira.go.ug/nira-api/1.0.0/verifyPersonInformation"
    response = requests.post(url, headers=headers, data=payload, verify=False).json()
    print(json.dumps(response))
    return HttpResponse(json.dumps(response), content_type='application/json')


def ursb(request,  *args, **kwargs):
    headers = {
    'Authorization': f'Bearer {str(ursb_token(request))}',
    'Cookie': '__NCTRACE=52a25b5d-04b1-4f99-b48d-35249629ffa6'
    }
    payload={}
    brn = request.POST.get('brn') 
    url = f"https://api-uat.integration.go.ug/t/ursb.go.ug/ursb-brs-api/1.0.0/entity/get_entity_full/{brn}/-/APS-NITA"
    xml_server_response = requests.get( url, headers=headers, data=payload )
    response = xmltodict.parse(xml_server_response.text)
    # print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


# ugpass 
def redirect_page(request):
    context = {}
    return render(request, "account/redirect.html", context)


def generateRequetJWT():
    # Create request parameter JWT Payload
    payload = {
    "iat": datetime.datetime.utcnow(),
    "iss": SCOPES['client_id'],
    "aud": URLS['ugpass_issuer'],
    "sub": SCOPES['client_id'],
    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    "redirect_uri": URLS['callback_uri'],
    }

    #Client/Service Provider Private Key for creating JWT Token
    try:
        # Create request parameter JWT Token
        request_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
        return request_jwt
    except Exception as error:
        print(error)
        return False


def buildAuthorizationURL(request_jwt):
    # Run this request authorization_redirect_url from a browser
    # Server will return an authorization code after the user is
    # prompted for credentials.

    #Generate state parameter(random string)
    state = secrets.token_urlsafe(13)

    #Generate nonce parameter(random string)
    nonce = secrets.token_urlsafe(15)

    authorization_redirect_url = URLS['authorize_url'] +'?response_type=code&client_id='+SCOPES['client_id']+'&redirect_uri='+URLS['callback_uri']+\
    '&scope='+ SCOPES['scope'] +'&state='+state +'&nonce='+nonce+\
    '&request='+request_jwt
    
    return authorization_redirect_url


def createClientAssertionToken():
    # # Create client_assertion parameter JWT Payload
    payload = {
        "iat": datetime.datetime.utcnow(),
        "iss": SCOPES['client_id'],
        "aud": URLS['token_url'],
        "sub": SCOPES['client_id'],
        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    }

    try:
        # Create ssertion JWT Token
        client_assertion_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
        return client_assertion_jwt
    except Exception as error:
        print(error)
        return False


def getAccessToken(authorization_code, client_assertion_jwt):
    # create Request Body
    payload = {
         'grant_type': 'authorization_code',
         'code': authorization_code,
         'redirect_uri': URLS['callback_uri'],
         'client_id':SCOPES['client_id'],
         'client_assertion_type':'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
         'client_assertion':client_assertion_jwt
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(URLS['token_url'], data=payload, headers=headers, verify=False, allow_redirects=False)
        tokens = json.loads(response.text)
        access_token = tokens['access_token']
        id_token = tokens['id_token']
        
        

        return access_token,id_token


    except Exception as err:
        print(err)
        return False, False


def getUserInfo(access_token):
    endpoint = URLS['user_info_url']
    info_headers = {
        "Accept": "application/jwt", 
        "Authorization": "Bearer {token}".format(token=access_token)
    }

    response = requests.get(endpoint, headers=info_headers, verify=False)
    return response.text


def ugpass(request, *args, **kwargs):
    if request.method == "GET":
        RequestToken = generateRequetJWT()
        if RequestToken:
            authorization_url = buildAuthorizationURL(RequestToken)
            return redirect(authorization_url)


def handle_redirect_url(request, *args, **kwargs):
    if request.method == "GET":
        state = request.GET.get('state', None)
        authorization_code = request.GET.get('code', None)

        #validate your state key
        client_assertion_jwt = createClientAssertionToken()
        the_access_token, id_token = getAccessToken(authorization_code, client_assertion_jwt)
        # user_data = getUserInfo(the_access_token)
        # print(user_data)

        jwks_client = jwt.PyJWKClient(URLS['jwks_url'])
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)

        decoded_id_token = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=SCOPES['client_id'],
            issuer=URLS['ugpass_issuer'],
            options={"verify_exp": True},
        )

        print(id_token)
        print(decoded_id_token)

        #check if email / phone exists in your application
        ugpass_email = decoded_id_token['daes_claims']['email']
        ugpass_phone = decoded_id_token['daes_claims']['phone']
        print(ugpass_email)
        landing_page = 'client:client_home'
        try:
            user = Account.objects.get(email=ugpass_email)
            #authenticate them in LGRB
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect(landing_page)

        except Account.DoesNotExist:
            return HttpResponse("Sorry, No Matching User Profile")





