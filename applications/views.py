from django.contrib import messages
from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, View, UpdateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from account.decorators import *
from django.template.loader import render_to_string, get_template
from applications.forms import *
from django.contrib import messages

from operator import and_
from django.db.models import Q
from applications.models import *
from config.utils import *

# pdf stuff
from django.contrib.staticfiles import finders
from io import BytesIO
from xhtml2pdf import pisa
import urllib3
import json

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

import locale
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_premise_licence_expiry_date(request):
    licence = PrincipleLicence.objects.all()

    for lin in licence:
        created_date = lin.date_applied
        expires_on = datetime.timedelta(days=360) + created_date

        expiry_date = expires_on
        lin.save()

        print(expires_on)

    return HttpResponse("Not working!")

def molgapikey():
    url = "https://api-uat.integration.go.ug/token?grant_type=client_credentials"
    payload = {}

    headers = {
    'Authorization': 'Basic aDZCckZyMnpTTmtZWUZGVDJvR2llV3p4WTQ4YTpranV5TWdUd3JsOWNEeURLdnViSFZFel9leUFh'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    accesstoken = res['access_token']
    return accesstoken


def getdistricts():
    accesstoken =  molgapikey()
    url = "https://api-uat.integration.go.ug/t/molg.go.ug/molg/1.0.0/districts?start&limit&name&region_id&sub_region_id"
    payload = {}
    headers = {
    'MOLG-AUD-Auth-Token': 'fTydZWdaEOAwIffZqrDyO4fYU9fPwM9koikoSIIHzq0bYyO7wOQxql4QsIulkQIx',
    'Authorization': 'Bearer '+ accesstoken }
    response = requests.request("GET", url, headers=headers, data=payload)
    res = json.loads(response.text)
    data = res['data']
    return data




decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=[ 'client'])]
class PrincipleLicenceCreate(View):

    template_name = 'new/principle/principle_licence.html'
    form_class = PrincipleLicenceForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        districts = getdistricts()
        
        context = {
            'form': form,
            'districts': districts
        }
        return render(request, self.template_name, context)

 
    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.applicant = request.user
                application.save()
                messages.success(request, 'licence applied successfully')
                return redirect('client:client_home')
            else:
                print(form.errors)
        return render(request, self.template_name, {'form': form})
    


decorators = [login_required(login_url='login'), allowed_users( allowed_roles=[ 'client'])]
@method_decorator(decorators, 'dispatch')
class PrincipleLicenceCreated(View):

    form_class = PrincipleLicenceForm
    template_name = 'new/principle/principle_licence.html'

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):

        if request.method == 'POST':

            data = json.loads(request.body)

            form = self.form_class(data, request.FILES)

            if form.is_valid():

                form.save()

                return JsonResponse({'success': True, 'message': 'Payment added successfully'})
            else:
                print(form.errors)
                return JsonResponse({'success': False, 'errors': form.errors})

    # def post(self, request):

    #     if request.method == 'POST':
    #         try:
    #             data = json.loads(request.body)
    #             form = self.form_class(data, request.FILES)
    #             if form.is_valid():
    #                 form.save()
    #                 return JsonResponse({'success': True, 'message': 'Payment added successfully'})
    #             else:
    #                 print(form.errors)
    #                 return JsonResponse({'success': False, 'errors': form.errors})
    #         except json.JSONDecodeError:
    #             return JsonResponse({'success': False, 'errors': 'Invalid JSON data'})
    #     else:
    #         return JsonResponse({'success': False, 'errors': 'Invalid request method'})
    


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier', 'approver', 'inspector', 'client'])]

@method_decorator(decorators, 'dispatch')
class PrincipleLicenceDetail(DetailView):
    model = PrincipleLicence
    template_name = 'new/principle/principle_licence_detail.html'
    context_object_name = 'licence'

    def get_object(self):
        object = get_object_or_404(PrincipleLicence, id=self.kwargs['id'])
        return object


decorators = [login_required(login_url='login'), never_cache,
              allowed_users(allowed_roles=['verifier', 'approver', 'inspector', 'admin'])]


@method_decorator(decorators, 'dispatch')
class PrincipleLicenceUpdate(UpdateView):
    model = PrincipleLicence
    fields = [
        'inspection_authority_status',
        'inspection_authority_remarks',
        'forward_for_verification',
        'evaluation_checklist',
        'defer_to_inspector',

        'verification_authority_status',
        'verification_authority_remarks',
        'forward_for_approval',
        'defer_to_verifier',

        'approving_authority_status',
        'approving_authority_remarks',
        'approved',

        'assigned_to_inspector',
        'manager_remarks',
        'date_assigned',

    ]
    # fields = "__all__"

    template_name = 'new/principle/principle_licence_update.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/licence/task/list'

    queryset = PrincipleLicence.objects.all()

    context_object_name = 'verified'


# new employee licence  

class EmployeeLicenceCreate(View):
 
    template_name = 'new/employee/employee_licence.html'
    form_class = EmployeeLicenceForm

    def get(self, request, *args, **kwargs):
        
        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.applicant = request.user
                application.save()
                messages.success(request, 'licence applied successfully')
                return redirect('applications:new_prn_list')
            else:
                print(form.errors)
        return render(request, self.template_name, {'form': form})
    


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier', 'approver', 'inspector', 'client'])]


@method_decorator(decorators, 'dispatch')
class EmployeeLicenceDetail(DetailView):
    model = EmployeeLicence
    context_object_name = 'keyemployee_detail'
    template_name = 'new/employee/employee_licence_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['keyemployee_detail'] = EmployeeLicence.objects.all()
        return context


decorators = [login_required(login_url='login'), never_cache,
              allowed_users(allowed_roles=['verifier', 'approver', 'inspector', 'admin'])]


@method_decorator(decorators, 'dispatch')
class EmployeeLicenceUpdate(UpdateView):
    model = EmployeeLicence
    fields = [
        'inspection_authority_status',
        'inspection_authority_remarks',
        'forward_for_verification',
        'verification_authority_status',
        'verification_authority_remarks',
        'forward_for_approval',
        'approving_authority_status',
        'approved',
        'assigned_to_inspector',
        'manager_remarks',
        'date_assigned',

    ]
    template_name = 'new/employee/employee_update.html'
    pk_url_kwarg = 'pk'
    success_url = '/licence/task/list'

    queryset = EmployeeLicence.objects.filter(
        Q(approved=False) & ~Q(approving_authority_status="Pending")

    )
    # get_object_or_404(queryset)
    # template_name_suffix = '_update_form'
    context_object_name = 'verified'


# premise licence 

def premise_list(request):
    premises = PremiseLicence.objects.filter(email=request.user.email)
    context = {
        'premises': premises
    }
    return render(request, 'new/premise/premise_list.html', context)


def save_all(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            premises = PremiseLicence.objects.all()
            data['premise_list'] = render_to_string('new/premise/premise_list_2.html', {'premises': premises})
        else:
            data['form_is_valid'] = False

    context = {'form': form}

    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def create_premise(request):
    if request.method == 'POST':
        form = PremisesForm(request.POST)
    else:
        form = PremisesForm()
    return save_all(request, form, 'new/premise/premise_create.html')


def premise_delete(request, id):
    data = dict()
    premise = get_object_or_404(PremiseLicence, id=id)
    if request.method == "POST":
        premise.delete()
        data['form_is_valid'] = True
        premise = PremiseLicence.objects.filter(email=request.user.email)
        data['premise_list'] = render_to_string('new/premise/premise_list_2.html', {'premise': premise})
    else:
        context = {'premise': premise}
        data['html_form'] = render_to_string('new/premise/premise_delete.html', context, request=request)

    return JsonResponse(data)


def premise_update(request, id):
    premise = get_object_or_404(PremiseLicence, id=id)
    if request.method == "POST":
        form = PremiseLicenceUpdateForm(request.POST, request.FILES, instance=premise)

    else:
        form = PremiseLicenceUpdateForm(instance=premise)
    return save_all(request, form, 'new/premise/premise_update.html')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier', 'approver', 'inspector', 'admin_officer', 'client'])]


@method_decorator(decorators, 'dispatch')
class CreatePremise(View):
    template_name = 'new/premise/premise_add.html'

    form_class = PremisesForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_class = PremisesForm(request.POST, request.FILES)
        form = form_class

        if form.is_valid():
            form.save()
            return redirect('applications:premise_list')

        return render(request, self.template_name, {'form': form})



decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier', 'approver', 'inspector', 'client'])]


@method_decorator(decorators, 'dispatch')
class PremiseLicenceDetail(DetailView):
    model = PremiseLicence
    context_object_name = 'premise_licence_detail'
    template_name = 'new/premise/premise_licence_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['premise_detail'] = PremiseLicence.objects.all()
        return context



class PremisePaymentList(View):
    template_name = 'new/premise/premise_payment_list.html'

    def get(self, request, *args, **kwargs):
        premise_payment = PremisePayment.objects.filter(email=request.user.email)
        context = {
            'premise_payment': premise_payment
        }

        return render(request, self.template_name, context)


class PremiseLicenceUpdate(UpdateView):
    model = PremiseLicence
    fields = [
        'inspection_authority_status',
        'inspection_authority_remarks',
        'forward_for_verification',
        'premise_inspection_report',

        'verification_authority_status',
        'verification_authority_remarks',
        'forward_for_approval',

        'approving_authority_status',
        'approved'
    ]

    template_name = 'new/premise/premise_licence_update.html'
    pk_url_kwarg = 'pk'
    success_url = '/licence/task/list'
    queryset = PremiseLicence.objects.all()

    context_object_name = 'verified'


"""  utils """
def get_premise_amount(request):
    if request.method == "POST":
        email = request.POST['email']
        # email = request.get.GET['email']
        # email = request.GET['email']
        nopremises = PremiseLicence.objects.filter(email=email)
        if nopremises.exists():
            counted = nopremises.count()
            message = {
                "code": 200,
                "message": "success",
                "count": counted
            }
            print(counted)
            return JsonResponse({'count': message})
        else:
            message = {
                "code": 404,
                "message": "error",
                "count": ""
            }

            return JsonResponse({'count': ''})


def get_principle_amount(request):
    if request.method == "POST":
        certificate_number = request.POST['principle_licence_certificate_number']
        print(certificate_number)
        approved_licence = PrincipleLicence.objects.filter(
            certificate_number=certificate_number, approved=True
        )

        if approved_licence:
            for licence in approved_licence:
                fees = licence.licence_fee
                tin = licence.tin

                message = {
                    "code": 200,
                    "message": "success",
                    "tin": tin,
                    "fee": fees
                }

                print(message)
                return JsonResponse({'fee': message})

        else:
            print("not found ")
            return HttpResponse("not found ")



def is_date_in_range(date):
    current_date = datetime.now().date()
    start_date = datetime(current_date.year, 10, 1).date()
    end_date = datetime(current_date.year, 12, 25).date()

    return start_date <= date <= end_date


def previous_principle_licence_data(request):

    if request.method == "POST":
        
        previous_licence_number = request.POST['previous_licence_number']
        print(previous_licence_number)
        approved_licence = PrincipleLicence.objects.filter(
            certificate_number=previous_licence_number,
        )

        if approved_licence:

            for licence in approved_licence:

                tin = licence.tin
                validity = licence.validity
                name_of_the_company = licence.name_of_the_company
                licence_fee = licence.licence_fee
                application_fee = licence.application_fee
                company_status = licence.company_status
                licence_type = licence.licence_type

                ura_district = licence.ura_district
                ura_county = licence.ura_county
                ura_subcounty = licence.ura_subcounty
                ura_village = licence.ura_village

                input_date = datetime.now().date()
                result = is_date_in_range(input_date)

                print(result)  # Output: True or False

                # if result == True:

                #     message = {
                #         "code": 200,
                #         "message": "success",
                #         "validity": validity,
                #         "tin": tin,
                #         "name_of_the_company": name_of_the_company,
                #         "company_status": company_status ,
                #         "licence_fee": licence_fee,
                #         "application_fee": application_fee,
                #         "licence_type": licence_type,

                #         "ura_district": ura_district,
                #         "ura_county": ura_county,
                #         "ura_subcounty": ura_subcounty,
                #         "ura_village": ura_village,
                #     }
                #     return JsonResponse({'response': message})
                
                # else:
                #     message = {
                #         "code": 200,
                #         "message": "error",
                #         "validity": validity,
                #         "tin": tin,
                #         "name_of_the_company": name_of_the_company,
                #         "company_status": company_status ,
                #         "licence_fee": licence_fee,
                #         "application_fee": application_fee,
                #         "licence_type": licence_type,

                #         "ura_district": ura_district,
                #         "ura_county": ura_county,
                #         "ura_subcounty": ura_subcounty,
                #         "ura_village": ura_village,
                        
                #     }
                #     return JsonResponse({'response': message})
                message = {
                        "code": 200,
                        "message": "success",
                        "validity": validity,
                        "tin": tin,
                        "name_of_the_company": name_of_the_company,
                        "company_status": company_status ,
                        "licence_fee": licence_fee,
                        "application_fee": application_fee,
                        "licence_type": licence_type,

                        "ura_district": ura_district,
                        "ura_county": ura_county,
                        "ura_subcounty": ura_subcounty,
                        "ura_village": ura_village,
                    }
                return JsonResponse({'response': message})
                

                
        else:
            print("not found ")
            return HttpResponse("not found ")


def previous_employee_licence_data(request):

    if request.method == "POST":
        
        previous_licence_number = request.POST['previous_licence_number']
        print(previous_licence_number)
        approved_licence = PrincipleLicence.objects.filter(
            certificate_number=previous_licence_number,
        )

        if approved_licence:
            for licence in approved_licence:
                tin = licence.tin
                name_of_the_company = licence.name_of_the_company
                licence_fee = licence.licence_fee
                company_status = licence.company_status
                licence_type = licence.licence_type

                message = {
                    "code": 200,
                    "message": "success",
                    "tin": tin,
                    "name_of_the_company": name_of_the_company,
                    "company_status": company_status ,
                    "licence_fee": licence_fee,
                    "licence_type": licence_type
                }

                print(message)
                return JsonResponse({'response': message})

        else:
            print("not found ")
            return HttpResponse("not found ") 



decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['client'])]


@method_decorator(decorators, 'dispatch')
class LicencePrns(View):
    template_name = 'new/prns/prns.html'

    def get(self, request, *args, **kwargs):
        context = {}

        new_principle_principle_licence_track = PrincipleLicence.objects.filter(
            email=request.user.email
        )
        new_keyemployee_licence_track = EmployeeLicence.objects.filter(
            email=request.user.email
        )
        new_premise_licence_track = PremiseLicence.objects.filter(
            email=request.user.email
        )

        context['new_principle_principle_licence_track'] = new_principle_principle_licence_track
        context['new_premise_licence_track'] = new_premise_licence_track
        context['new_keyemployee_licence_track'] = new_keyemployee_licence_track

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['client'])]
@method_decorator(decorators, 'dispatch')
class NewCertificateList(View):
    template_name = 'new/certificate/new_certificate.html'

    def get(self, request, *args, **kwargs):
        context = {}

        new_principle_certificate = PrincipleLicence.objects.filter(
            Q( approving_authority_status="Approved" ),
            Q( bank_guarantee__approving_authority_status="Approved" ),
            Q( applicationfeepayments__payment_description = "RECEIVED AND CREDITED") | Q( licencefeepayments__payment_description = "RECEIVED AND CREDITED") ,
            Q( email=request.user.email ),

        )
        new_premise_certificate = PremiseLicence.objects.filter(
            approving_authority_status="Approved",
            approved=True,
            email=request.user.email,
        )

        new_keyemployee_certificate = EmployeeLicence.objects.filter(
            approving_authority_status="Approved",
            approved=True,
            email=request.user.email,

        )

        print(new_keyemployee_certificate)

        context['new_principle_certificate'] = new_principle_certificate
        context['new_premise_certificate'] = new_premise_certificate
        context['new_keyemployee_certificate'] = new_keyemployee_certificate

        return render(request, self.template_name, context)


def format_currency(amount, currency_symbol):
    formatted_amount = "{:,.2f} {}".format(amount, currency_symbol)
    return formatted_amount
    

def generate_token():
    headers = {
        'Authorization': 'Basic bDNxTkFGRVphQVg2Nkg1aEE4ZjA3REpreFNBYTpqUGZIZ2FxZ2trUjd3ZmtRWlRpTUU5MzB5NUlh', }
    data = {'grant_type': 'client_credentials'}
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


def check_premise_licence_fee_status(request):
    """
    Query the latest 3 records where the payment_status has not been updated
    """
    licenses = EmployeeLicence.objects.filter(
        Q(payment_status__isnull=True) | Q(payment_status__iexact='') | Q(payment_description__isnull=True) |
        Q(payment_description__iexact='') | Q(payment_description="AVAILABLE") | Q(
            payment_description="EXPIRED")).order_by('-date_applied')[:3]

    if licenses:

        for license in licenses:

            response = check_clearance_status(license.prn)  # returns URA API response
            if 'CheckPRNStatusResult' in response and 'StatusCode' in response[
                'CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
                license.payment_status = response['CheckPRNStatusResult'][
                    'StatusCode']  # you can retrieve any records you want from the API
                license.payment_description = response['CheckPRNStatusResult']['StatusDesc']
                license.save()  # save to database
            else:
                license.payment_status = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusCode']
                license.payment_description = response['CheckPRNStatusResponse']['CheckPRNStatusResult']['StatusDesc']
                license.save()

    return HttpResponse("working")


def view_pdf(request, pk):
    # Get the premise object
    premise = get_object_or_404(PremiseLicence, pk=pk)
    
    # Create a file-like buffer to receive PDF data.
    buffer = HttpResponse(content_type='application/pdf')

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    stylesheet=getSampleStyleSheet()
    # normalStyle = stylesheet['Normal']

     # Set the background image
    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_premise.jpg"
    p.drawImage(
        bg_image_path,
        0, 0,
        width=p._pagesize[0], 
        height=p._pagesize[1]
    )

    # Render the book image if available
    # if premise.signature:
    #     img_data = premise.signature  # Assuming the image data is saved as a binary string in the 'image' field
    #     # byteImgIO = io.BytesIO()

    #     img = ImageReader(io.BytesIO(img_data))

    #     p.drawImage(img, 100, 500, width=2*inch, height=2*inch)

    # p.drawString(100-- left and right, 700 --up and down, f"{premise.id}")

    p.drawString(
        50, 785, 
        f"{premise.id}"
    )
    
    # p.drawString( 150, 410, f"{premise.operator_name} T/A FORTBET " )

    p.setFont('Helvetica-Oblique', 13)
    p.drawCentredString(p._pagesize[0] / 2, 410, f"{premise.operator_name} T/A FORTBET ")
    p.drawCentredString(p._pagesize[0] / 2, 348,  f"Plot {premise.plot_number}" )
    p.drawCentredString(p._pagesize[0] / 2, 330,  f" {premise.premise_name} " )
    p.drawCentredString(p._pagesize[0] / 2, 300,  f" {premise.district} District , {premise.region} Region  {premise.municipality} Municipality ")

    p.drawCentredString(p._pagesize[0] / 2, 276,  f" {premise.date_applied} " )
    p.drawCentredString(p._pagesize[0] / 2, 258,  f" to the " )
    p.drawCentredString(p._pagesize[0] / 2, 240,  f" {premise.date_applied}" )
    p.drawCentredString(p._pagesize[0] / 2, 222,  f"Dated at {premise.date_approved} " )

    # locale.setlocale( locale.LC_ALL, 'en_UG' )
    # premise_fee = locale.currency(premise.inspection_fee, grouping=True,  symbol=True, international=True )
    # p.drawString( 300 , 300, premise_fee)

    # p.drawString( 300, 348,   f"Plot {premise.plot_number}" )
    # p.drawString( 250, 330,   f" {premise.building_name} Building" )

    p.showPage()
    p.save()

    return buffer


def download_pdf(request, pk):
    # Get the book object
    book = get_object_or_404(PremiseLicence, pk=pk)
    
    # Create a file-like buffer to receive PDF data.
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw the book details on the PDF.
    p.drawString(100, 800, f"Title: {book.title}")
    p.drawString(100, 750, f"Author: {book.author}")
    p.drawString(100, 700, f"ISBN: {book.isbn}")
    p.drawString(100, 650, f"Price: {book.price}")
    p.drawString(100, 600, f"Description: {book.description}")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return buffer



""" certificates  """

def certificate_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('id')
    certificate = get_object_or_404(EmployeeLicence, pk=pk)
    template_path = 'client/pdf_certificate.html'
    context = {'certificate': certificate}
    response = HttpResponse(content_type='application/pdf')
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def certificate_pdf_download_view(request, *args, **kwargs):
    pk = kwargs.get('id')
    certificate = get_object_or_404(EmployeeLicence, pk=pk)
    template_path = 'new/certificate/pdf_certificate.html'
    context = {'certificate': certificate}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def principle_certificate_pdf_view(request, pk, *args, **kwargs):

    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PrincipleLicence, pk=pk)
    # template_path = 'new/certificate/pdf_principle_certificate.html'

    # context = {
    #     'certificate': certificate
    # }

    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    principle = get_object_or_404(PrincipleLicence, pk=pk)    
    buffer = HttpResponse(content_type='application/pdf')
    p = canvas.Canvas(buffer)
    # p.setFont('Helvetica', 12)
    


    if principle.licence_type == "License to conduct a Public Lottery":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_casino.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to conduct a public lottery within Uganda from the" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )
        
        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved.strftime('%Y')}-12-31  " )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "License to conduct a National Lottery":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_casino.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to conduct a national lottery within Uganda from the" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Casino operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/template_casino.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to establish or operate a casino within Uganda from " )
        p.drawCentredString(p._pagesize[0] / 2, 330,  f" {principle.date_applied}  to {principle.date_approved.strftime('%Y')}-12-31 " )
        p.drawCentredString(p._pagesize[0] / 2, 300,  f" The licensee is authorised to employ __________ (persons) ")

        p.drawCentredString(p._pagesize[0] / 2, 276,  f" as the minimum number of employees. " )
        p.drawCentredString(p._pagesize[0] / 2, 258,  f" The class of casino games played in the casino shall be limited to:" )
        p.drawCentredString(p._pagesize[0] / 2, 240,  f" {principle.class_of_the_casino_games}" )
        p.drawCentredString(p._pagesize[0] / 2, 222,  f"Dated at {principle.date_approved} " )
    

    elif principle.licence_type == "Pool betting license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_pool.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to provide facilities for pool or pool operating license within Uganda from" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )
  
  
    elif principle.licence_type == "Bingo betting license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bingo.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to provide facilities for bingo or bingo operating license within Uganda from" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Betting Intermediary operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bil.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        
        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed to provide gaming or facilities for betting other than pool betting " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "or general betting operating licence, a gaming or betting machine techinical operating licence,  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "a betting intermediary operating licence, within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved} " )


        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )
    

    elif principle.licence_type == "Gaming or betting machine techinical operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bmtol.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")

        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed to manufacture, supply, install, adapt, mantain or repair a gaming or  " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "betting machine or part of a gaming or betting machine or  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "betting machine technical operating licence, within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "General betting operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_generalbetting.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 360,  "is licensed to provide facilities for betting other than pool betting or " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "general betting operating licence with Uganda from the" )
        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 240,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Gambling software operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_software.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")

        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed  to manufacture, supply, install or adapt gambling software or " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "a gambling software operating licence  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Gaming or betting machine general operating license":

        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bmtol.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")

        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed to manufacture, supply, install, adapt, mantain or repair a gaming or  " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "betting machine or part of a gaming or betting machine or  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "betting machine technical operating licence, within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved.strftime('%Y')}-12-31 " )

        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )

    else:
        p.drawCentredString(p._pagesize[0] / 2, 240,  f"Dated at {principle.date_approved} " )

    p.showPage()
    p.save()

    return buffer


def principle_certificate_pdf_download_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PrincipleLicence, pk=pk)
    # template_path = 'new/certificate/pdf_principle_certificate.html'
    # context = {
    #     'certificate': certificate
    # }
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    principle = get_object_or_404(PrincipleLicence, pk=pk)    
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="{principle.name_of_the_company}.pdf"'

    p = canvas.Canvas(buffer)
    # p.setFont('Helvetica', 12)
    


    if principle.licence_type == "License to conduct a Public Lottery":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_casino.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to conduct a public lottery within Uganda from the" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )
        
        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved}" )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "License to conduct a National Lottery":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_casino.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to conduct a national lottery within Uganda from the" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved}" )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Casino operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/template_casino.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to establish or operate a casino within Uganda from " )
        p.drawCentredString(p._pagesize[0] / 2, 330,  f" {principle.date_applied}  to {principle.date_approved.strftime('%Y')}-12-31 " )
        p.drawCentredString(p._pagesize[0] / 2, 300,  f" The licensee is authorised to employ __________ (persons) ")

        p.drawCentredString(p._pagesize[0] / 2, 276,  f" as the minimum number of employees. " )
        p.drawCentredString(p._pagesize[0] / 2, 258,  f" The class of casino games played in the casino shall be limited to:" )
        p.drawCentredString(p._pagesize[0] / 2, 240,  f" {principle.class_of_the_casino_games}" )
        p.drawCentredString(p._pagesize[0] / 2, 222,  f"Dated at {principle.date_approved} " )
    

    elif principle.licence_type == "Pool betting license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_pool.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to provide facilities for pool or pool operating license within Uganda from" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved}" )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )
  
  
    elif principle.licence_type == "Bingo betting license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bingo.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to provide facilities for bingo or bingo operating license within Uganda from" )
        p.drawCentredString(p._pagesize[0] / 2, 320,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  f" {principle.date_approved}" )

        p.drawCentredString(p._pagesize[0] / 2, 260,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Betting Intermediary operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bil.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        
        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed to provide gaming or facilities for betting other than pool betting " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "or general betting operating licence, a gaming or betting machine techinical operating licence,  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "a betting intermediary operating licence, within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved} " )


        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )
    

    elif principle.licence_type == "Gaming or betting machine techinical operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_bmtol.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")

        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed to manufacture, supply, install, adapt, mantain or repair a gaming or  " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "betting machine or part of a gaming or betting machine or  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "betting machine technical operating licence, within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved} " )

        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "General betting operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_generalbetting.png"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")
        p.drawCentredString(p._pagesize[0] / 2, 360,  "is licensed to provide facilities for betting other than pool betting or " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "general betting operating licence with Uganda from the" )
        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )

        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved}" )

        p.drawCentredString(p._pagesize[0] / 2, 240,  f"Dated at Kampala {principle.date_approved} " )


    elif principle.licence_type == "Gambling software operating license":
        bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_software.jpg"
        p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )
        p.drawString(50, 785, f"{principle.id}")
        p.setFont('Helvetica-Oblique', 13)
        p.drawCentredString(p._pagesize[0] / 2, 410, f"{principle.name_of_the_company} T/A MAYFAIR CASINO ")

        p.drawCentredString(p._pagesize[0] / 2, 380,  "is licensed  to manufacture, supply, install or adapt gambling software or " )
        p.drawCentredString(p._pagesize[0] / 2, 360,  "a gambling software operating licence  " )
        p.drawCentredString(p._pagesize[0] / 2, 340,  "within Uganda from the " )

        p.drawCentredString(p._pagesize[0] / 2, 300,  f" {principle.date_applied} " )
        p.drawCentredString(p._pagesize[0] / 2, 280,  " to " )
        p.drawCentredString(p._pagesize[0] / 2, 260,  f" {principle.date_approved} " )

        p.drawCentredString(p._pagesize[0] / 2, 220,  f"Dated at Kampala {principle.date_approved} " )

    else:
        p.drawCentredString(p._pagesize[0] / 2, 240,  f"Dated at {principle.date_approved} " )

    p.showPage()
    p.save()

    return buffer


def employee_certificate_pdf_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(EmployeeLicence, pk=pk)
    # template_path = 'new/certificate/pdf_employee_certificate.html'

    # context = {
    #     'certificate': certificate
    # }

    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    premise = get_object_or_404(EmployeeLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    # buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/employee/template_employee.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )

    p.drawString( 50, 785, f"{premise.id}" )
   
    p.setFont('Helvetica-Oblique', 13)

    # trade_name = str(premise.trade_name).upper()

    p.drawCentredString(p._pagesize[0] / 2, 410, f"{premise.name_of_the_company} T/A BETPAWA ")
    p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to be employeed in a casino, Gaming or  " )
    p.drawCentredString(p._pagesize[0] / 2, 330,  " Betting facility within Uganda from the " )
    
    p.drawCentredString(p._pagesize[0] / 2, 276,  f" {premise.date_applied} " )
    p.drawCentredString(p._pagesize[0] / 2, 258,  f" to the " )
    p.drawCentredString(p._pagesize[0] / 2, 240,  f"{premise.date_approved.strftime('%Y')}-12-31 ")
    p.drawCentredString(p._pagesize[0] / 2, 222,  f"Dated at {premise.date_approved} " )

    p.showPage()
    p.save()

    return buffer


def employee_certificate_pdf_download_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(EmployeeLicence, pk=pk)
    # template_path = 'new/certificate/pdf_employee_certificate.html'
    # context = {
    #     'certificate': certificate
    # }
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    premise = get_object_or_404(EmployeeLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)
    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/employee/template_employee.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1] )

    p.drawString( 50, 785, f"{premise.id}" )
    p.setFont('Helvetica-Oblique', 13)

    # trade_name = str(premise.trade_name).upper()

    p.drawCentredString(p._pagesize[0] / 2, 410, f"{premise.name_of_the_company} T/A BETPAWA ")
    p.drawCentredString(p._pagesize[0] / 2, 348,  "is licensed to be employeed in a casino, Gaming or  " )
    p.drawCentredString(p._pagesize[0] / 2, 330,  " Betting facility within Uganda from the " )
    
    p.drawCentredString(p._pagesize[0] / 2, 276,  f" {premise.date_applied} " )
    p.drawCentredString(p._pagesize[0] / 2, 258,  f" to the " )
    p.drawCentredString(p._pagesize[0] / 2, 240,  f" {premise.date_approved.strftime('%Y')}-12-31 " )
    p.drawCentredString(p._pagesize[0] / 2, 222,  f"Dated at {premise.date_approved} " )

    p.showPage()
    p.save()

    return buffer


def premise_certificate_pdf_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PremiseLicence, pk=pk)
    # template_path = 'new/certificate/pdf_premise_certificate.html'

    # context = {
    #     'certificate': certificate
    # }

    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    # Get the premise object
    premise = get_object_or_404(PremiseLicence, pk=pk)
    
    buffer = HttpResponse(content_type='application/pdf')
    # buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/certificate/principle/template_premise.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    # Render the book image if available
    # if premise.signature:
    #     img_data = premise.signature  # Assuming the image data is saved as a binary string in the 'image' field
    #     # byteImgIO = io.BytesIO()

    #     img = ImageReader(io.BytesIO(img_data))

    #     p.drawImage(img, 100, 500, width=2*inch, height=2*inch)

    # p.drawString(100-- left and right, 700 --up and down, f"{premise.id}")

    p.drawString(
        50, 785, 
        f"{premise.id}"
    )
    
    # p.drawString( 150, 410, f"{premise.operator_name} T/A FORTBET " )

    p.setFont('Helvetica-Oblique', 13)

    trade_name = str(premise.trade_name).upper()

    p.drawCentredString(p._pagesize[0] / 2, 410, f"{premise.operator_name} T/A {trade_name} ")
    p.drawCentredString(p._pagesize[0] / 2, 348,  f"Plot {premise.plot_number}" )
    p.drawCentredString(p._pagesize[0] / 2, 330,  f" {premise.premise_name} " )
    p.drawCentredString(p._pagesize[0] / 2, 300,  f" {premise.district} District , {premise.region} Region  {premise.municipality} Municipality ")

    p.drawCentredString(p._pagesize[0] / 2, 276,  f" {premise.date_applied} " )
    p.drawCentredString(p._pagesize[0] / 2, 258,  f" to the " )
    p.drawCentredString(p._pagesize[0] / 2, 240,  f" {premise.date_approved.strftime('%Y')}-12-31 " )
    p.drawCentredString(p._pagesize[0] / 2, 222,  f"Dated at {premise.date_approved} " )

    # locale.setlocale( locale.LC_ALL, 'en_UG' )
    # premise_fee = locale.currency(premise.inspection_fee, grouping=True,  symbol=True, international=True )
    # p.drawString( 300 , 300, premise_fee)

    # p.drawString( 300, 348,   f"Plot {premise.plot_number}" )
    # p.drawString( 250, 330,   f" {premise.building_name} Building" )

    p.showPage()
    p.save()

    return buffer
    

def premise_certificate_pdf_download_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    certificate = get_object_or_404(PremiseLicence, pk=pk)
    template_path = 'new/certificate/pdf_premise_certificate.html'
    context = {
        'certificate': certificate
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



"""  Prn """

def principle_prn_application_fee_pdf_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PrincipleLicence, pk=pk)
    # template_path = 'new/prns/principle_applicationfee_prnslip.html'
    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)
    # context = {
    #     'certificate': certificate
    # }
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # # if pisa_status.err:
    # #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    slip = get_object_or_404(PrincipleLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{slip.name_of_the_company}" )
    p.drawString( 35, 670, f"{slip.ura_district}" )
    p.drawString( 35, 655, f"{slip.ura_county}" )
    p.drawString( 35, 640, f"{slip.ura_subcounty}" )
    p.drawString( 35, 625, f"{slip.ura_village}" )

  
    if slip.licence_type  == "License to conduct a National Lottery":
        p.drawString( 95, 578, "APPLICATION FEE FOR A LICENCE TO CONDUCT A NATIONAL LOTTERY " )
    elif slip.licence_type == "License to conduct a Public Lottery":
        p.drawString( 95, 578, "APPLICATION FEE FOR A LICENCE TO CONDUCT A PUBLIC LOTTERY " )
    elif slip.licence_type == "Casino operating license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR A LICENE TO ESTABLISH OR OPERATE A CASINO"  )  
    elif slip.licence_type == "Bingo betting license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A LICENSE TO PROVIDE FACILITIES FOR BINGO BETTING" )
    elif slip.licence_type == "Pool betting license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR A LICENSE TO PROVIDE FACILITIES FOR POOL BETTING " )
    elif slip.licence_type == "Betting Intermediary operating license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR  A BETTING INTERMEDIARY OPERATING LICENCE" )
    elif slip.licence_type == "Gaming or betting machine general operating license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A BETTING MACHINE GENERAL OPERATING LICENCE" )
    elif slip.licence_type == "Gaming or betting machine techinical operating license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR A BETTING MACHINE TECHINICAL OPERATING LICENCE"  )
    elif slip.licence_type == "General betting operating license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A GENERAL BETTING LICENCE"  )
    elif slip.licence_type == "Gambling software operating license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A SOFTWARE OPERATING LICENCE "  )
    else:
        pass 

    # application fees formatting

    currency_symbol = "UGX"
    application_fee = format_currency(slip.applicationfeepayments.application_fee, currency_symbol)


    p.drawString( 130, 547, application_fee )
    p.drawString( 435, 547, application_fee )
    # applicationfeepayments
    # licencefeepayments
    p.drawString( 435, 525, f" {slip.applicationfeepayments.tin}" )
    p.drawString( 455, 505, f" {slip.applicationfeepayments.prn}" )
    
    p.drawString( 95, 565, f"{slip.company_status.upper()} APPLICANT" )
    
    p.drawString( 155, 483, f" {slip.date_applied}" )
    p.drawString( 365, 483, f" {slip.applicationfeepayments.payment_expiry_date}" )
    # general 
    p.drawString( 380, 180, f" {slip.applicant.phone_number}" )
    p.drawString( 380, 150, f" {slip.applicant.email}" )

    p.showPage()
    p.save()
    return buffer


def principle_prn_application_fee_pdf_download_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PrincipleLicence, pk=pk)
    # template_path = 'new/prns/principle_applicationfee_prnslip.html'
    # context = {
    #     'certificate': certificate
    # }
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    slip = get_object_or_404(PrincipleLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="{slip.id}.pdf"'
    
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{slip.name_of_the_company}" )
    p.drawString( 35, 670, f"{slip.ura_district}" )
    p.drawString( 35, 655, f"{slip.ura_county}" )
    p.drawString( 35, 640, f"{slip.ura_subcounty}" )
    p.drawString( 35, 625, f"{slip.ura_village}" )

  
    if slip.licence_type  == "License to conduct a National Lottery":
        p.drawString( 95, 578, "APPLICATION FEE FOR A LICENCE TO CONDUCT A NATIONAL LOTTERY " )
    elif slip.licence_type == "License to conduct a Public Lottery":
        p.drawString( 95, 578, "APPLICATION FEE FOR A LICENCE TO CONDUCT A PUBLIC LOTTERY " )
    elif slip.licence_type == "Casino operating license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR A LICENE TO ESTABLISH OR OPERATE A CASINO"  )  
    elif slip.licence_type == "Bingo betting license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A LICENSE TO PROVIDE FACILITIES FOR BINGO BETTING" )
    elif slip.licence_type == "Pool betting license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR A LICENSE TO PROVIDE FACILITIES FOR POOL BETTING " )
    elif slip.licence_type == "Betting Intermediary operating license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR  A BETTING INTERMEDIARY OPERATING LICENCE" )
    elif slip.licence_type == "Gaming or betting machine general operating license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A BETTING MACHINE GENERAL OPERATING LICENCE" )
    elif slip.licence_type == "Gaming or betting machine techinical operating license":
        p.drawString( 95, 578,  "APPLICATION FEE FOR A BETTING MACHINE TECHINICAL OPERATING LICENCE"  )
    elif slip.licence_type == "General betting operating license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A GENERAL BETTING LICENCE"  )
    elif slip.licence_type == "Gambling software operating license":
        p.drawString( 95, 578, "APPLICATION FEE FOR A SOFTWARE OPERATING LICENCE "  )
    else:
        pass 

    # application fees formatting

    currency_symbol = "UGX"
    application_fee = format_currency(slip.application_fee, currency_symbol)

    p.drawString( 130, 547, application_fee )
    p.drawString( 435, 547, application_fee )
    # applicationfeepayments
    # licencefeepayments
    p.drawString( 435, 525, f" {slip.applicationfeepayments.tin}" )
    p.drawString( 455, 505, f" {slip.applicationfeepayments.prn}" )
    p.drawString( 95, 565, f"{slip.company_status.upper()} APPLICANT" )
    p.drawString( 155, 483, f" {slip.date_applied}" )
    p.drawString( 365, 483, f" {slip.applicationfeepayments.payment_expiry_date}" )
    # general 
    p.drawString( 380, 180, f" {slip.applicant.phone_number}" )
    p.drawString( 380, 150, f" {slip.applicant.email}" )

    p.showPage()
    p.save()
    return buffer


def principle_prn_licence_fee_pdf_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PrincipleLicence, pk=pk)
    # # certificate = PrincipleLicence.objects.filter(id=pk)
    # template_path = 'new/prns/principle_licencefee_prnslip.html'
    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)
    # context = {
    #     'certificate': certificate
    # }
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # # if pisa_status.err:
    # #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    slip = get_object_or_404(PrincipleLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    # buffer['Content-Disposition'] = f'attachment; filename="{slip.premise_name}.pdf"'
    
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{slip.name_of_the_company}" )
    p.drawString( 35, 670, f"{slip.ura_district}" )
    p.drawString( 35, 655, f"{slip.ura_county}" )
    p.drawString( 35, 640, f"{slip.ura_subcounty}" )
    p.drawString( 35, 625, f"{slip.ura_village}" )


    if slip.licence_type  == "License to conduct a National Lottery":
        p.drawString( 95, 578, "LICENSE FEE FOR A LICENSE TO CONDUCT A NATIONAL LOTTERY ")
            
    elif slip.licence_type == "License to conduct a Public Lottery":
        p.drawString( 95, 578, "LICENSE FEE FOR A LICENSE TO CONDUCT A PUBLIC LOTTERY" )
        
    elif slip.licence_type == "Casino operating license":
        p.drawString( 95, 578,  "LICENSE FEE FOR A LICENE TO ESTABLISH OR OPERATE A CASINO" )
            
    elif slip.licence_type == "Bingo betting license":
        p.drawString( 95, 578,  "LICENSE FEE FOR A LICENSE TO PROVIDE FACILITIES FOR BINGO BETTING" )
            
    elif slip.licence_type == "Pool betting license":
        p.drawString( 95, 578,  "LICENSE FEE FOR A LICENSE TO PROVIDE FACILITIES FOR POOL BETTING" )
        
    elif slip.licence_type == "Betting Intermediary operating license":
        p.drawString( 95, 578,  "LICENSE FEE FOR  A BETTING INTERMEDIARY OPERATING LICENCE" )
        
    elif slip.licence_type == "Gaming or betting machine general operating license":
        p.drawString( 95, 578,  "LICENSE FEE FOR A BETTING MACHINE GENERAL OPERATING LICENCE")
        
    elif slip.licence_type == "Gaming or betting machine techinical operating license":
        p.drawString( 95, 578,  "LICENSE FEE FOR BETTING MACHINE TECHNICAL OPERATING LICENCE")
        
    elif slip.licence_type == "General betting operating license":
        p.drawString( 95, 578,  "LICENSE FEE FOR A GENERAL BETTING LICENCE" )
        
    elif slip.licence_type == "Gambling software operating license":
        p.drawString( 95, 578,  "LICENSE FEE FOR GAMBLING SOFTWARE OPERATING LICENCE" )
        
    else:
        pass

    currency_symbol = "UGX"
    licence_fee = format_currency(slip.licencefeepayments.licence_fee, currency_symbol)


    p.drawString( 130, 547, licence_fee )
    p.drawString( 435, 547, licence_fee )


    p.drawString( 435, 525, f" {slip.licencefeepayments.licence_fee_tin}" )
    p.drawString( 455, 505, f" {slip.licencefeepayments.licence_fee_prn}" )

    p.drawString( 95, 565, f"{slip.company_status.upper()} APPLICANT" )

    p.drawString( 155, 483, f" {slip.date_applied}" )
    p.drawString( 365, 483, f" {slip.licencefeepayments.payment_expiry_date}" )

    # general 
    p.drawString( 380, 180, f" {slip.applicant.phone_number}" )
    p.drawString( 380, 150, f" {slip.applicant.email}" )

    p.showPage()
    p.save()
    return buffer


def principle_prn_licence_fee_pdf_download_view(request, *args, **kwargs):
    pk = kwargs.get('id')
    certificate = get_object_or_404(PrincipleLicence, pk=pk)
    template_path = 'new/prns/principle_licencefee_prnslip.html'
    context = {
        'certificate': certificate
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def employee_prn_pdf_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(EmployeeLicence, pk=pk)
    # template_path = 'new/prns/employee_prnslip.html'

    # context = {
    #     'certificate': certificate
    # }

    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    premise = get_object_or_404(EmployeeLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    # buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'

    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{premise.name_of_the_company}" )
    p.drawString( 35, 670, f"{premise.ura_district}" )
    p.drawString( 35, 655, f"{premise.ura_county}" )
    p.drawString( 35, 640, f"{premise.ura_subcounty}" )
    p.drawString( 35, 625, f"{premise.ura_village}" )

    p.drawString( 95, 578, "APPLICATION FOR A SPECIAL EMPLOYEE LICENSE" )

    currency_symbol = "UGX"
    application_fee = format_currency(premise.application_fee, currency_symbol)

    p.drawString( 130, 547, application_fee )
    p.drawString( 435, 547, application_fee )

    p.drawString( 435, 525, f" {premise.tin}" )
    p.drawString( 455, 505, f" {premise.prn}" )

    p.drawString( 155, 483, f" {premise.date_applied}" )
    p.drawString( 365, 483, f" {premise.payment_expiry_date}" )

    p.drawString( 380, 180, f" {request.user.phone_number}" )
    p.drawString( 380, 150, f" {request.user.email}" )

    p.showPage()
    p.save()

    return buffer


def new_employee_prn_pdf_download_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(EmployeeLicence, pk=pk)
    # template_path = 'new/prns/employee_penslip.html'
    # context = {
    #     'certificate': certificate
    # }
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    premise = get_object_or_404(EmployeeLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'

    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{premise.name_of_the_company}" )
    p.drawString( 35, 670, f"{premise.ura_district}" )
    p.drawString( 35, 655, f"{premise.ura_county}" )
    p.drawString( 35, 640, f"{premise.ura_subcounty}" )
    p.drawString( 35, 625, f"{premise.ura_village}" )

    p.drawString( 95, 578, "APPLICATION FOR A SPECIAL EMPLOYEE LICENSE" )

    currency_symbol = "UGX"
    application_fee = format_currency(premise.application_fee, currency_symbol)

    p.drawString( 130, 547, application_fee )
    p.drawString( 435, 547, application_fee )

    p.drawString( 435, 525, f" {premise.tin}" )
    p.drawString( 455, 505, f" {premise.prn}" )

    p.drawString( 155, 483, f" {premise.date_applied}" )
    p.drawString( 365, 483, f" {premise.payment_expiry_date}" )

    p.drawString( 380, 180, f" {request.user.phone_number}" )
    p.drawString( 380, 150, f" {request.user.email}" )

    p.showPage()
    p.save()

    return buffer


def premise_prn_pdf_view(request, pk,  *args, **kwargs):
    
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PremiseLicence, pk=pk)
    # template_path = 'new/prns/premise_prnslip.html'
    # context = {
    #     'certificate': certificate
    # }

    # response = HttpResponse(content_type='application/pdf')
    # template = get_template(template_path)

    # context = {
    #     'certificate': certificate
    # }

    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # # if pisa_status.err:
    # #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    premise = get_object_or_404(PremiseLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    # buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'

    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{premise.operator_name}" )
    p.drawString( 35, 670, f"{premise.ura_district}" )
    p.drawString( 35, 655, f"{premise.ura_county}" )
    p.drawString( 35, 640, f"{premise.ura_subcounty}" )
    p.drawString( 35, 625, f"{premise.ura_village}" )

    p.drawString( 95, 578, "INSPECTION AND APPROVAL FEES FOR ESTABLISHING A BRANCH " )

    currency_symbol = "UGX"
    inspection_fee = format_currency(premise.inspection_fee, currency_symbol)

    p.drawString( 130, 547, inspection_fee )
    p.drawString( 435, 547, inspection_fee )

    p.drawString( 435, 525, f" {premise.tin}" )
    p.drawString( 455, 505, f" {premise.prn}" )

    p.drawString( 155, 483, f" {premise.date_applied}" )
    p.drawString( 365, 483, f" {premise.payment_expiry_date}" )

    p.drawString( 380, 180, f" {request.user.phone_number}" )
    p.drawString( 380, 150, f" {request.user.email}" )

    p.showPage()
    p.save()

    return buffer


def premise_prn_pdf_download_view(request, pk, *args, **kwargs):
    # pk = kwargs.get('id')
    # certificate = get_object_or_404(PremiseLicence, pk=pk)
    # template_path = 'new/prns/premise_prnslip.html'
    # context = {
    #     'certificate': certificate
    # }
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # template = get_template(template_path)
    # html = template.render(context)
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

    premise = get_object_or_404(PremiseLicence, pk=pk)
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="{premise.premise_name}.pdf"'

    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 12)

    bg_image_path = "http://uat.els.lgrb.go.ug/static/assets/img/slip.jpg"
    p.drawImage( bg_image_path, 0, 0, width=p._pagesize[0],  height=p._pagesize[1] )

    p.setFont('Helvetica', 9.5)
    p.drawString( 35, 685, f"{premise.operator_name}" )
    p.drawString( 35, 670, f"{premise.ura_district}" )
    p.drawString( 35, 655, f"{premise.ura_county}" )
    p.drawString( 35, 640, f"{premise.ura_subcounty}" )
    p.drawString( 35, 625, f"{premise.ura_village}" )

    p.drawString( 95, 578, "INSPECTION AND APPROVAL FEES FOR ESTABLISHING A BRANCH " )

    currency_symbol = "UGX"
    inspection_fee = format_currency(premise.inspection_fee, currency_symbol)

    p.drawString( 130, 547, inspection_fee )
    p.drawString( 435, 547, inspection_fee )

    p.drawString( 435, 525, f" {premise.tin}" )
    p.drawString( 455, 505, f" {premise.prn}" )

    p.drawString( 155, 483, f" {premise.date_applied}" )
    p.drawString( 365, 483, f" {premise.payment_expiry_date}" )

    p.drawString( 380, 180, f" {request.user.phone_number}" )
    p.drawString( 380, 150, f" {request.user.email}" )

    p.showPage()
    p.save()

    return buffer


