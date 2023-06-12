from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import View
from .models import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from account.decorators import *
from django.template.loader import render_to_string
from new.forms import *
from django.contrib import messages

from functools import reduce
from operator import and_ 
from django.db.models import Q

from datetime import datetime, timedelta
from payments.forms import *

decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['client'])]
@method_decorator(decorators, 'dispatch')
class ClientView(View):

    template_name = 'client/client_home.html'

    application_fees_form_class = ApplicationFeePaymentForm 
    licence_fees_form_class = LicenceFeePaymentForm

    def get(self, request, *args, **kwargs):
        context = {}

        licence_fees_form = self.licence_fees_form_class()
        application_fees_form = self.application_fees_form_class()
    
        context['application_fees_form'] = application_fees_form
        context['licence_fees_form'] = licence_fees_form

        new_principle_principle_licence_track = PrincipleLicence.objects.filter(
            email=request.user.email
        ).order_by('-date_applied')
        new_keyemployee_licence_track = EmployeeLicence.objects.filter(
            email=request.user.email
        ).order_by('-date_applied')
        new_premise_licence_track = PremiseLicence.objects.filter(
            email=request.user.email
        ).order_by('-date_applied')
        
        context['new_principle_principle_licence_track'] = new_principle_principle_licence_track
        context['new_premise_licence_track'] = new_premise_licence_track
        context['new_keyemployee_licence_track'] = new_keyemployee_licence_track

        # approved
        principle_approved_by_inspector = PrincipleLicence.objects.filter(
            email=request.user.email,
            inspection_authority_status = "Recomended for a licence",
            forward_for_verification = True
        ).count()
        employee_approved_by_inspector   = EmployeeLicence.objects.filter(
            email=request.user.email,
            inspection_authority_status = "Recomended for a licence",
            forward_for_verification = True
        ).count()
        premise_approved_by_inspector = PremiseLicence.objects.filter(
           email=request.user.email,
            inspection_authority_status = "Recomended for a licence",
            forward_for_verification = True
        ).count()
       
        # rejected
        principle_rejected_by_inspector = PrincipleLicence.objects.filter(
            email=request.user.email,
            inspection_authority_status = "Does not meet creteria",
            forward_for_verification = True
        ).count()
        employee_rejected_by_inspector   = EmployeeLicence.objects.filter(
           email=request.user.email,
            inspection_authority_status = "Does not meet creteria",
            forward_for_verification = True
        ).count()
        premise_rejected_by_inspector = PremiseLicence.objects.filter(
           email=request.user.email,
            inspection_authority_status = "Does not meet creteria",
            forward_for_verification = True
        ).count()
       
        # new applications
        new_principle_licence = PrincipleLicence.objects.filter(
            email=request.user.email,
            inspection_authority_status = None,
            forward_for_verification = False
        ).count()
        new_employee_licence   = EmployeeLicence.objects.filter(
             email=request.user.email,
            inspection_authority_status = None,
            forward_for_verification = False
        ).count()
        new_premise_licence = PremiseLicence.objects.filter(
            email=request.user.email,
            inspection_authority_status = None,
            forward_for_verification = False
        ).count()

        context['total_approved_by_inspector'] = principle_approved_by_inspector + employee_approved_by_inspector + premise_approved_by_inspector
        context['total_rejected_by_inspector'] = principle_rejected_by_inspector + employee_rejected_by_inspector + premise_rejected_by_inspector
        context['new_pplications'] = new_principle_licence + new_employee_licence + new_premise_licence
        
        # dashboard statistics
        return render(request, self.template_name, context)
        
