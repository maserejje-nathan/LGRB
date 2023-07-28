from ast import Bytes, Not
import email
from multiprocessing import context
from re import template
from django.contrib import messages
from django.http import FileResponse, Http404
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, View, UpdateView, DetailView, ListView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from account.decorators import *
from new.forms import *

from functools import reduce
from operator import and_ 
from django.db.models import Q

from new.models import *
from bankguarantee.models import *
from bankguarantee.forms import *


# new bank guarantee 

decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['verifier', 'approver', 'admin_officer', 'client' ])]
@method_decorator(decorators, 'dispatch')
class BankGuaranteeCreate(View):

    template_name = 'bankguarantee/new/new_bank_guarantee_create.html'
    form_class  = BankGuaranteeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form_class = BankGuaranteeForm(request.POST, request.FILES)
        form = form_class

        # create the payment and update the payment foeld in the db.

        if form.is_valid():
            bank_guarantee_attachment = form.save(commit=False)
            certificate_no = form.cleaned_data.get('principle_licence_certificate_number')
            bank_guarantee_attachment.save()
            if bank_guarantee_attachment:
                principle_license = PrincipleLicence.objects.filter(Q(certificate_number=certificate_no)).first()
                if principle_license:
                    principle_license.bank_guarantee = bank_guarantee_attachment
                    principle_license.save()
                    messages.success(request, 'Bank guarantee has been submitted successfully')
                    return redirect('client:client_home')
        return render(request, self.template_name, {'form': form})


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['verifier', 'approver', 'admin_officer', 'client'])]
@method_decorator(decorators, 'dispatch')
class BankGuaranteeList(View):
    
    template_name = 'bankguarantee/new/new_bank_guarantee_list.html'

    def get(self, request, *args, **kwargs):

        context = {}  

        # client docket
        context['client_bank_guarantee_list'] = BankGuarantee.objects.filter(
            email=request.user.email
        )

        #  Verification docket 
        context['bank_guarantee_at_verification'] = BankGuarantee.objects.filter(

            # Q(inspection_authority_status = "Recomended for a licence") | Q( inspection_authority_status = "Recomended for rejection"),

            Q(verification_authority_status = None ),
            # Q(forward_for_approval = False),

            Q(approving_authority_status = None),
            # Q(approved = False),

        ) 

        # approval docket
        context['bank_guarantee_at_approval'] = BankGuarantee.objects.filter(

            Q(verification_authority_status = "Recomended for approval") | Q( verification_authority_status = "Recomended for rejection"),
            # Q(forward_for_approval = True), 

            # Q(approving_authority_status = "Approved") | Q( verification_authority_status = "Recomended for rejection"),
            # Q(forward_for_approval = True), 
            # Q(approved = False)  
            
        )

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),  allowed_users(allowed_roles=['verifier', 'approver'])]
@method_decorator(decorators, 'dispatch')
class BankGuaranteeUpdate(UpdateView):
    model = BankGuarantee
    fields = [
        # verification officer
        'verification_authority_status', 
        'verification_authority_remarks', 
        'verified_by',
        # 'forward_for_approval',
        # 'date_verified', 

        # approving officer 
        'approving_authority_status', 
        'approving_authority_remarks',
        # 'approved', 
       
        # 'date_approved' 
    ]
    template_name = 'bankguarantee/new/new_bank_guarantee_update.html'
    pk_url_kwarg = 'pk'
    success_url = '/bankguaranteee/new/list'

    queryset = BankGuarantee.objects.all() 

    context_object_name = 'verified'


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['client'])]
@method_decorator(decorators, 'dispatch')
class BankGuaranteeDetail(View):
    template_name = 'bankguarantee/new_bank_guarantee_detail.html'


    def get(self, request, *args, **kwargs):

        # bill_types = PrincipleLicence.objects.all()
        # bills = BankGuarantee.objects.select_related('bill_type').all()

        context = {}
        bankguarantee = get_object_or_404(PrincipleLicence, pk=kwargs.get('pk'))
        context["bankguarantee"] = bankguarantee
        return render(request, self.template_name, context)




# renewed bank guarantee 

decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['verifier', 'approver', 'admin_officer', 'client' ])]
@method_decorator(decorators, 'dispatch')
class RenewedBankGuaranteeCreate(View):

    template_name = 'bankguarantee/renewed/renew_bank_guarantee_create.html'
    form_class  = BankGuaranteeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form_class = BankGuaranteeForm(request.POST, request.FILES)
        form = form_class

        # create the payment and update the payment foeld in the db.

        if form.is_valid():
            bank_guarantee_attachment = form.save(commit=False)
            certificate_no = form.cleaned_data.get('principle_licence_certificate_number')
            bank_guarantee_attachment.save()
            if bank_guarantee_attachment:
                principle_license = PrincipleLicence.objects.filter(Q(certificate_number=certificate_no)).first()
                if principle_license:
                    principle_license.bank_guarantee = bank_guarantee_attachment
                    principle_license.save()
                    messages.success(request, 'Bank guarantee has been submitted successfully')
                
        return render(request, self.template_name, {'form': form})


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['verifier', 'approver', 'admin_officer', 'client'])]
@method_decorator(decorators, 'dispatch')
class RenewedBankGuaranteeList(View):
    
    template_name = 'bankguarantee/renewed/renew_bank_guarantee_list.html'

    def get(self, request, *args, **kwargs):

        context = {}        
        #  Verification docket 
        context['bank_guarantee_at_verification'] = BankGuarantee.objects.filter(

            # Q(inspection_authority_status = "Recomended for a licence") | Q( inspection_authority_status = "Recomended for rejection"),

            Q(verification_authority_status = None ),
            # Q(forward_for_approval = False),

            Q(approving_authority_status = None),
            # Q(approved = False),

        ) 

        # approval docket
        context['bank_guarantee_at_approval'] = BankGuarantee.objects.filter(

            Q(verification_authority_status = "Recomended for approval") | Q( verification_authority_status = "Recomended for rejection"),
            # Q(forward_for_approval = True), 

            # Q(approving_authority_status = "Approved") | Q( verification_authority_status = "Recomended for rejection"),
            # Q(forward_for_approval = True), 
            # Q(approved = False)  
            
        )

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),  allowed_users(allowed_roles=['verifier', 'approver'])]
@method_decorator(decorators, 'dispatch')
class RenewedBankGuaranteeUpdate(UpdateView):
    model = BankGuarantee
    fields = [
        # verification officer
        'verification_authority_status', 
        'verification_authority_remarks', 
        'verified_by',
        'forward_for_approval',
        # 'date_verified', 

        # approving officer 
        'approving_authority_status', 
        'approving_authority_remarks',
        'approved', 
       
        # 'date_approved' 
    ]
    template_name = 'bankguarantee/renewed/renew_bank_guarantee_update.html'
    pk_url_kwarg = 'pk'
    success_url = '/bankguaranteee/new/list'

    queryset = BankGuarantee.objects.all() 

    context_object_name = 'verified'


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['client'])]
@method_decorator(decorators, 'dispatch')
class RenewedBankGuaranteeDetail(View):
    template_name = 'bankguarantee/renewed/renew_bank_guarantee_detail.html'


    def get(self, request, *args, **kwargs):

        # bill_types = PrincipleLicence.objects.all()
        # bills = BankGuarantee.objects.select_related('bill_type').all()

        context = {}
        bankguarantee = get_object_or_404(PrincipleLicence, pk=kwargs.get('pk'))
        context["bankguarantee"] = bankguarantee
        return render(request, self.template_name, context)



