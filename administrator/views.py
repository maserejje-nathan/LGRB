from account.decorators import allowed_users
from django.shortcuts import render, redirect
from django.views.generic import  UpdateView, View

from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from functools import reduce
from operator import and_
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from new.forms import *
from client.models import *

from account.models import *
from account.forms import AdminRegistrationForm
from administrator.forms import *

from django.utils import timezone

from reportlab.pdfgen import canvas
from django.http import HttpResponse

# # inspecting officer
# inspection_authority_status
# inspected_by
# forward_for_verification

# # verification officer
# verification_authority_status
# verified_by
# forward_for_approval


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')

class CompanyListView(View):
    # template_name = 'administrator/users/company.html'
    template_name = 'administrator/users/company_new.html'

    def get(self, request, *args, **kwargs):

        admins_list = Account.objects.filter(
            Q(role="client"),
            Q(legalStatus="Company" )
        )
        total_admin_count = Account.objects.filter(
            Q(role = "inspector") | Q(role = "verifier") | Q(role = "approver") | Q(role = "admin")

        ).count()
        
        total_clients = Account.objects.filter(
            role = "client"
        ).count()
  
        
        total_inspectors = Account.objects.filter(
            role = "inspector"
        ).count()
    

        total_verifiers = Account.objects.filter(
            role = "verifier"
        ).count()

        total_approvers = Account.objects.filter(
            role = "approver"
        ).count()

        total_admins = Account.objects.filter(
            role = "admin"
        ).count()

        total_users = Account.objects.all().count()

        percentage_total_clients = (total_clients / total_users) * 100
        percentage_total_inspectors = ( total_inspectors / total_users) * 100
        percentage_total_verifiers = ( total_verifiers / total_users) * 100
        percentage_total_approvers = (total_approvers / total_users) * 100
        percentage_total_admins = (total_admins / total_users) * 100

        # print("new_total_clients:" ,new_total_clients)
        # print("new_total_inspectors:" ,new_total_inspectors)
        # print("new_total_verifiers:" ,new_total_verifiers)
        # print("new_total_approvers:" ,new_total_approvers)
        # print("new_total_admins:" ,new_total_admins)
        # print(new_total_clients + new_total_inspectors + new_total_verifiers + new_total_approvers + new_total_admins)

        all_total_roles = [ total_admins,total_clients,  total_inspectors, total_verifiers, total_approvers, ]


        total = Account.objects.all()

        page = request.GET.get('page', 1)

        paginator = Paginator(admins_list, 10)
        try:
            admins = paginator.page(page)
        except PageNotAnInteger:
            admins = paginator.page(1)
        except EmptyPage:
            admins = paginator.page(paginator.num_pages)

        return render(request, self.template_name,{
            'admins': admins,
            'total_clients': total_clients,
            'total_inspectors': total_inspectors,
            'total_verifiers': total_verifiers,
            'total_admins': total_admins,
            'total_admin_count': total_admin_count,
            'total_users': total_users,
            'total': total,
            'all_total_roles': all_total_roles,

            "percentage_total_clients":   percentage_total_clients, 
            "percentage_total_inspectors":percentage_total_inspectors, 
            "percentage_total_verifiers": percentage_total_verifiers,  
            "percentage_total_approvers": percentage_total_approvers, 
            "percentage_total_admins":    percentage_total_admins,  
         })


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')

class CompanyDetailView(View):
    template_name = 'administrator/users/company-detail.html'

    def get(self, request, *args, **kwargs):
        detail = Account.objects.filter(legalStatus="Company")
        context = {
            'detail': detail
        }
        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')

class IndividualListView(View):
    # template_name = 'administrator/users/individual.html'
    template_name = 'administrator/users/individual_new.html'
    # paginate_by = 10

    def get(self, request, *args, **kwargs):

        admins_list = Account.objects.filter(
            Q(role="client"),
            Q(legalStatus="Individual" )
        )
        total_admin_count = Account.objects.filter(
            Q(role = "inspector") | Q(role = "verifier") | Q(role = "approver") | Q(role = "admin")

        ).count()

        total_clients = Account.objects.filter(
            role = "client"
        ).count()
  
        
        total_inspectors = Account.objects.filter(
            role = "inspector"
        ).count()
    

        total_verifiers = Account.objects.filter(
            role = "verifier"
        ).count()

        total_approvers = Account.objects.filter(
            role = "approver"
        ).count()

        total_admins = Account.objects.filter(
            role = "admin"
        ).count()

        total_users = Account.objects.all().count()

        percentage_total_clients = (total_clients / total_users) * 100
        percentage_total_inspectors = ( total_inspectors / total_users) * 100
        percentage_total_verifiers = ( total_verifiers / total_users) * 100
        percentage_total_approvers = (total_approvers / total_users) * 100
        percentage_total_admins = (total_admins / total_users) * 100

        # print("new_total_clients:" ,new_total_clients)
        # print("new_total_inspectors:" ,new_total_inspectors)
        # print("new_total_verifiers:" ,new_total_verifiers)
        # print("new_total_approvers:" ,new_total_approvers)
        # print("new_total_admins:" ,new_total_admins)
        # print(new_total_clients + new_total_inspectors + new_total_verifiers + new_total_approvers + new_total_admins)

        all_total_roles = [ total_admins,total_clients,  total_inspectors, total_verifiers, total_approvers, ]


        total = Account.objects.all()

        page = request.GET.get('page', 1)

        paginator = Paginator(admins_list, 10)
        try:
            admins = paginator.page(page)
        except PageNotAnInteger:
            admins = paginator.page(1)
        except EmptyPage:
            admins = paginator.page(paginator.num_pages)

        return render(request, self.template_name,{
            'admins': admins,
            'total_clients': total_clients,
            'total_inspectors': total_inspectors,
            'total_verifiers': total_verifiers,
            'total_admins': total_admins,
            'total_admin_count': total_admin_count,
            'total_users': total_users,
            'total': total,
            'all_total_roles': all_total_roles,

            "percentage_total_clients":   percentage_total_clients, 
            "percentage_total_inspectors":percentage_total_inspectors, 
            "percentage_total_verifiers": percentage_total_verifiers,  
            "percentage_total_approvers": percentage_total_approvers, 
            "percentage_total_admins":    percentage_total_admins,  
         })


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')

class IndividualDetailView(View):
    template_name = 'administrator/users/individual-detail.html'

    def get(self, request, *args, **kwargs):
        context = {}
        individuals = Account.objects.all()
        context['individuals'] = individuals
        return render(request, self.template_name, context)



decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')

class AdminListView(View):
    # template_name = 'administrator/users/admin.html'
    template_name = 'administrator/users/admin_new.html'
    # paginate_by = 10 

    def get(self, request, *args, **kwargs):

        admins_list = Account.objects.filter(
            Q(role="inspector") | Q(role="verifier") | Q(role="approver") | Q(role="admin")
        )
        total_admin_count = Account.objects.filter(
            Q(role = "inspector") | Q(role = "verifier") | Q(role = "approver") | Q(role = "admin")

        ).count()

        total_clients = Account.objects.filter(
            role = "client"
        ).count()
  
        
        total_inspectors = Account.objects.filter(
            role = "inspector"
        ).count()
    

        total_verifiers = Account.objects.filter(
            role = "verifier"
        ).count()

        total_approvers = Account.objects.filter(
            role = "approver"
        ).count()

        total_admins = Account.objects.filter(
            role = "admin"
        ).count()

        total_users = Account.objects.all().count()

        percentage_total_clients = (total_clients / total_users) * 100
        percentage_total_inspectors = ( total_inspectors / total_users) * 100
        percentage_total_verifiers = ( total_verifiers / total_users) * 100
        percentage_total_approvers = (total_approvers / total_users) * 100
        percentage_total_admins = (total_admins / total_users) * 100

        # print("new_total_clients:" ,new_total_clients)
        # print("new_total_inspectors:" ,new_total_inspectors)
        # print("new_total_verifiers:" ,new_total_verifiers)
        # print("new_total_approvers:" ,new_total_approvers)
        # print("new_total_admins:" ,new_total_admins)
        # print(new_total_clients + new_total_inspectors + new_total_verifiers + new_total_approvers + new_total_admins)

        all_total_roles = [ total_admins,total_clients,  total_inspectors, total_verifiers, total_approvers, ]


        total = Account.objects.all()

        page = request.GET.get('page', 1)

        paginator = Paginator(admins_list, 10)
        try:
            admins = paginator.page(page)
        except PageNotAnInteger:
            admins = paginator.page(1)
        except EmptyPage:
            admins = paginator.page(paginator.num_pages)

        return render(request, self.template_name,{
            'admins': admins,
            'total_clients': total_clients,
            'total_inspectors': total_inspectors,
            'total_verifiers': total_verifiers,
            'total_admins': total_admins,
            'total_admin_count': total_admin_count,
            'total_users': total_users,
            'total': total,
            'all_total_roles': all_total_roles,

            "percentage_total_clients":   percentage_total_clients, 
            "percentage_total_inspectors":percentage_total_inspectors, 
            "percentage_total_verifiers": percentage_total_verifiers,  
            "percentage_total_approvers": percentage_total_approvers, 
            "percentage_total_admins":    percentage_total_admins,  
         })


decorators = [login_required(login_url='login'), allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')

class AdminDetailView(View):
    template_name = 'administrator/users/admin-detail.html'
    
    def get(self, request, *args, **kwargs): 
        
        context = {}
        admin = Account.objects.get(pk=kwargs.get('pk'))
        context['admin'] = admin
        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['admin'])]


@method_decorator(decorators, 'dispatch')
class Archives(View):

    template_name = 'administrator/archives.html'

    def get(self, request, *args, **kwargs):
        context = {}

        context['licences'] = PrincipleLicence.objects.all()

        # list only applications assigned to by the admin officer
        licences = PrincipleLicence.objects.all()

        # licences that are yet to be acted upoun
        # licence acted upoun
        # assigned and verification signature is false

        inspected = PrincipleLicence.objects.filter(inspected_by=request.user)
        signed = PrincipleLicence.objects.filter(forward_for_verification=True)
        assignment_status = PrincipleLicence.objects.all()

        archived_task = licence and assignment_status and signed

        if archived_task:
            messages.success(
                request, 'you have been assigned the licence to inspect bellow ')

        context['licences'] = licences
        context['assignment_status'] = assignment_status
        context['archived_task'] = archived_task

        return render(request, self.template_name, context)

    def post(request, self, *args, **kwargs):
        pass


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['admin'])]


@method_decorator(decorators, 'dispatch')
class AdminRegisterView(View):
    template_name = 'administrator/users/user_add.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = AdminRegistrationForm()
        context['admin_registration_form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = AdminRegistrationForm(request.POST)
        data = {}
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            # account = authenticate(email=email, password=raw_password)
            # login(request, account)
            messages.success(request, "user added successfully")
            print(messages.success(request, "user added successfully"))
        else:
            errors = form.errors
            messages.warning(request, errors)
            print(messages.warning(request, errors))
        context['admin_registration_form'] = form
        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'), allowed_users(
    allowed_roles=['admin', 'inspector', 'verifier', 'approver'])]


@method_decorator(decorators, 'dispatch')
class NewLicenceTaskList(View):

    template_name = 'administrator/tasks/principle_licence_list.html'

    def get(self, request, *args, **kwargs):

        context = {}

        #  inspectors achives
        context['achived_principle_licence_at_inspection'] = PrincipleLicence.objects.filter(
            # Q(inspection_authority_status = None) | Q(verification_authority_status = "Defered" ) | Q(forward_for_verification = False),
            # Q(forward_for_verification = False),
            assigned_to_inspector=request.user,

        )

        context['achived_premise_licence_at_inspection'] = PremiseLicence.objects.filter(
            inspection_authority_status=None,
            forward_for_verification=False
            #    assigned_to_inspector
        )

        context['achived_employee_licence_at_inspection'] = EmployeeLicence.objects.filter(
            inspection_authority_status=None,
            forward_for_verification=False,
            #  assigned_to_inspector = request.user

        )

        #  Verification achives
        context['achived_principle_licence_at_verification'] = PrincipleLicence.objects.filter(

            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(approving_authority_status="Defered"),
            Q(forward_for_verification=True),

            # assigned_to_verifier

            Q(verification_authority_status=None),
            Q(forward_for_approval=False),


        )

        context['achived_premise_licence_at_verification'] = PremiseLicence.objects.filter(
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True,

            #    assigned_to_verifier

            verification_authority_status=None,
            forward_for_approval=False,
        )

        context['achived_employee_licence_at_verification'] = EmployeeLicence.objects.filter(
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True,
            # assigned_to_verifier

            verification_authority_status=None,
            forward_for_approval=False,
        )

        # approval achives
        context['achived_principle_licence_at_approval'] = PrincipleLicence.objects.filter(

            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection"),
            Q(forward_for_verification=True),

            Q(verification_authority_status="Recomended for approval") | Q(
                verification_authority_status="Recomended for rejection"),
            Q(forward_for_approval=True),
            Q(approved=False),


        )

        context['achived_premise_licence_at_approval'] = PremiseLicence.objects.filter(
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True,

            verification_authority_status="Recomended for approval",
            forward_for_approval=True,

            approved=False
        )

        context['achived_employee_licence_at_approval'] = EmployeeLicence.objects.filter(
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True,

            verification_authority_status="Recomended for approval",
            forward_for_approval=True,

            approved=False
        )

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['admin'])]


@method_decorator(decorators, 'dispatch')
class NewInspectionAssignment(View):

    template_name = 'administrator/assign/assign_inspector_list.html'

    def get(self, request, *args, **kwargs):
        context = {}

        new_principle_licence_assignment = PrincipleLicence.objects.all()
        new_keyemployee_licence_assignment = EmployeeLicence.objects.all()
        new_premise_licence_assignment = PremiseLicence.objects.all()

        context['new_principle_licence_assignment'] = new_principle_licence_assignment
        context['new_keyemployee_licence_assignment'] = new_keyemployee_licence_assignment
        context['new_premise_licence_assignment'] = new_premise_licence_assignment

        # return render(request, self.template_name, {'admins': admins })

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['inspector'])]


@method_decorator(decorators, 'dispatch')
class InspectingAuthorityView(View):

    template_name = 'administrator/inspecting_officer_home.html'

    def get(self, request):


        context = {}

        # counts and statistics
        # employee assigned count 
        total_assigned_principle_licence = PrincipleLicence.objects.filter(
            Q(forward_for_verification = False),
            Q(assigned_to_inspector = request.user ),
            Q(assigned = True)

        ).count()

        total_assigned_employee_licence = EmployeeLicence.objects.filter(
            
            Q(assigned_to_inspector = request.user ),
            Q(assigned = True)

        ).count()

        total_assigned_premise_licence = PremiseLicence.objects.filter(
             Q(forward_for_verification = False),
            Q(assigned_to_inspector = request.user ),
            Q(assigned = True)

        ).count()


        total_licence_assigned = total_assigned_principle_licence +  total_assigned_employee_licence + total_assigned_premise_licence
        context['total_assigned_principle_licence'] = total_assigned_principle_licence
        context['total_assigned_employee_licence'] = total_assigned_employee_licence
        context['total_assigned_premise_licence'] = total_assigned_premise_licence

        context['total_licence_assigned'] = total_licence_assigned


        # approved
        principle_approved_by_inspector = PrincipleLicence.objects.filter(
            # verified_by = request.user
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True

        ).count()
        employee_approved_by_inspector = EmployeeLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True
        ).count()
        premise_approved_by_inspector = PremiseLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status="Recomended for a licence",
            forward_for_verification=True
        ).count()

        # rejected
        principle_rejected_by_inspector = PrincipleLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status="Does not meet creteria",
            forward_for_verification=True
        ).count()
        employee_rejected_by_inspector = EmployeeLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status="Does not meet creteria",
            forward_for_verification=True
        ).count()
        premise_rejected_by_inspector = PremiseLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status="Does not meet creteria",
            forward_for_verification=True
        ).count()

        # new applications
        new_principle_licence = PrincipleLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status=None,
            forward_for_verification=False
        ).count()
        new_employee_licence = EmployeeLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status=None,
            forward_for_verification=False
        ).count()
        new_premise_licence = PremiseLicence.objects.filter(
            # verified_by = request.user,
            inspection_authority_status=None,
            forward_for_verification=False
        ).count()

        context['total_approved_by_inspector'] = principle_approved_by_inspector + \
            employee_approved_by_inspector + premise_approved_by_inspector
        context['total_rejected_by_inspector'] = principle_rejected_by_inspector + \
            employee_rejected_by_inspector + premise_rejected_by_inspector
        context['new_pplications'] = new_principle_licence + \
            new_employee_licence + new_premise_licence

        #  inspectors docket
        context['principle_licence_at_inspection'] = PrincipleLicence.objects.filter(
            Q(inspection_authority_status=None) | Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_inspector=True),
            Q(forward_for_verification=False),
            Q(assigned_to_inspector=request.user)
        )

        context['premise_licence_at_inspection'] = PremiseLicence.objects.filter(
            Q(inspection_authority_status=None) | Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_inspector=True),
            Q(forward_for_verification=False),
            Q(assigned_to_inspector=request.user)
        )

        context['employee_licence_at_inspection'] = EmployeeLicence.objects.filter(
            Q(inspection_authority_status=None) | Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_inspector=True),
            Q(forward_for_verification=False),
            Q(assigned_to_inspector=request.user)
        )

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class VerificationAuthorityView(View):

    template_name = 'administrator/verification_officer_home.html'

    def get(self, request, *args, **kwargs):

        context = {}

        # counts and statistics 
        total_principle_licence_at_verification_licence = PrincipleLicence.objects.filter(
            
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_verifier=True),
            Q(forward_for_verification=True),

            Q(verification_authority_status=None) | Q(verification_authority_status="Recomended for a licence") | Q(
                verification_authority_status="Recomended for a rejection") | Q(verification_authority_status="Defered") | Q(approving_authority_status="Defered"),
            Q(forward_for_approval=False),

        ).count()

        total_employee_licence_at_verification = EmployeeLicence.objects.filter(
            
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_verifier=True),
            Q(forward_for_verification=True),

            Q(verification_authority_status=None) | Q(verification_authority_status="Recomended for a licence") | Q(
                verification_authority_status="Recomended for a rejection") | Q(verification_authority_status="Defered") | Q(approving_authority_status="Defered"),
            Q(forward_for_approval=False),

        ).count()

        total_premise_licence_at_verification = PremiseLicence.objects.filter(
            
            Q(inspection_authority_status="Recomended for a licence") | Q(inspection_authority_status="Recomended for rejection") | Q(defer_to_verifier=True),
            Q(forward_for_verification=True),

            Q(verification_authority_status=None) | Q(verification_authority_status="Recomended for a licence") | Q(
                verification_authority_status="Recomended for a rejection") | Q(verification_authority_status="Defered") | Q(approving_authority_status="Defered"),
            Q(forward_for_approval=False),

        ).count()

        

        total_licence_at_verification = total_principle_licence_at_verification_licence +  total_employee_licence_at_verification + total_premise_licence_at_verification
        
        context['total_principle_licence_at_verification_licence'] = total_principle_licence_at_verification_licence
        context['total_employee_licence_at_verification'] = total_employee_licence_at_verification
        context['total_premise_licence_at_verification'] = total_premise_licence_at_verification

        context['total_licence_at_verification'] = total_licence_at_verification



        # approved
        principle_approved_by_verifier = PrincipleLicence.objects.filter(
            # verified_by = request.user
            verification_authority_status="Recomended for approval",
            forward_for_approval=True

        ).count()
        employee_approved_by_verifier = EmployeeLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Recomended for approval",
            forward_for_approval=True
        ).count()
        premise_approved_by_verifier = PremiseLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Recomended for approval",
            forward_for_approval=True
        ).count()

        # rejected
        principle_rejected_by_verifier = PrincipleLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Recomended for rejection",
            forward_for_approval=True
        ).count()
        employee_rejected_by_verifier = EmployeeLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Recomended for rejection",
            forward_for_approval=True
        ).count()
        premise_rejected_by_verifier = PremiseLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Recomended for rejection",
            forward_for_approval=True
        ).count()

        # defered
        principle_defered_by_verifier = PrincipleLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Defered",
            forward_for_approval=True
        ).count()
        employee_defered_by_verifier = EmployeeLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Defered",
            forward_for_approval=True
        ).count()
        premise_defered_by_verifier = PremiseLicence.objects.filter(
            # verified_by = request.user,
            verification_authority_status="Defered",
            forward_for_approval=True
        ).count()

        context['total_approved_by_verifier'] = principle_approved_by_verifier + \
            employee_approved_by_verifier + premise_approved_by_verifier
        context['total_rejected_by_verifier'] = principle_rejected_by_verifier + \
            employee_rejected_by_verifier + premise_rejected_by_verifier
        context['total_defered_by_verifier'] = principle_defered_by_verifier + \
            employee_defered_by_verifier + premise_defered_by_verifier

        #  Verification docket
        context['principle_licence_at_verification'] = PrincipleLicence.objects.filter(
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_verifier=True),
            Q(forward_for_verification=True),

            Q(verification_authority_status=None) | Q(verification_authority_status="Recomended for a licence") | Q(
                verification_authority_status="Recomended for a rejection") | Q(verification_authority_status="Defered") | Q(approving_authority_status="Defered"),
            Q(forward_for_approval=False),

        )
        

        context['premise_licence_at_verification'] = PremiseLicence.objects.filter(
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_verifier=True),
            Q(forward_for_verification=True),

            Q(verification_authority_status=None) | Q(verification_authority_status="Recomended for a licence") | Q(
                verification_authority_status="Recomended for a rejection") | Q(verification_authority_status="Defered") | Q(approving_authority_status="Defered"),
            Q(forward_for_approval=False),

        )

        context['employee_licence_at_verification'] = EmployeeLicence.objects.filter(
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection") | Q(defer_to_verifier=True),
            Q(forward_for_verification=True),

            Q(verification_authority_status=None) | Q(verification_authority_status="Recomended for a licence") | Q(
                verification_authority_status="Recomended for a rejection") | Q(verification_authority_status="Defered") | Q(approving_authority_status="Defered"),
            Q(forward_for_approval=False),

        )

        return render(request, self.template_name, context)


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['approver'])]


@method_decorator(decorators, 'dispatch')
class ApprovingAuthorityView(View):
    template_name = 'administrator/approving_officer_home.html'

    def get(self, request, *args, **kwargs):

        context = {}

        # approved
        principle_approved_by_approver = PrincipleLicence.objects.filter(
            approved=True,
            approving_authority_status="Approved",
        ).count()
        employee_approved_by_approver = EmployeeLicence.objects.filter(
            # inspected_by = request.user,
            approved=True,
            approving_authority_status="Approved",
        ).count()
        premise_approved_by_approver = PremiseLicence.objects.filter(
            # inspected_by = request.user,
            approved=True,
            approving_authority_status="Approved"
        ).count()
        context['total_approved_by_approver'] = principle_approved_by_approver + \
            employee_approved_by_approver + premise_approved_by_approver

        # rejected
        principle_rejected_by_approver = PrincipleLicence.objects.filter(
            approved=False,
            approving_authority_status="Rejected",
        ).count()
        employee_rejected_by_approver = EmployeeLicence.objects.filter(
            # inspected_by = request.user,
            approved=False,
            approving_authority_status="Rejected",
        ).count()
        premise_rejected_by_approver = PremiseLicence.objects.filter(
            approved=False,
            approving_authority_status="Rejected"
        ).count()
        context['total_rejected_by_approver'] = principle_rejected_by_approver + \
            employee_rejected_by_approver + premise_rejected_by_approver

        # rejected
        principle_defered_by_approver = PrincipleLicence.objects.filter(
            approved=False,
            approving_authority_status="Defered",
        ).count()
        employee_defered_by_approver = EmployeeLicence.objects.filter(
            # inspected_by = request.user,
            approved=False,
            approving_authority_status="Defered",
        ).count()
        premise_defered_by_approver = PremiseLicence.objects.filter(
            approved=False,
            approving_authority_status="Defered"
        ).count()
        context['total_defered_by_approver'] = principle_defered_by_approver + \
            employee_defered_by_approver + premise_defered_by_approver

        # approval docket
        context['principle_licence_at_approval'] = PrincipleLicence.objects.filter(

            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection"),
            Q(forward_for_verification=True),

            Q(verification_authority_status="Recomended for approval") | Q(
                verification_authority_status="Recomended for rejection"),
            Q(forward_for_approval=True),

            approved=False
        )

        context['premise_licence_at_approval'] = PremiseLicence.objects.filter(
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection"),
            Q(forward_for_verification=True),

            Q(verification_authority_status="Recomended for approval") | Q(
                verification_authority_status="Recomended for rejection"),
            Q(forward_for_approval=True),

            approved=False
        )

        context['employee_licence_at_approval'] = EmployeeLicence.objects.filter(
            Q(inspection_authority_status="Recomended for a licence") | Q(
                inspection_authority_status="Recomended for rejection"),
            Q(forward_for_verification=True),

            Q(verification_authority_status="Recomended for approval") | Q(
                verification_authority_status="Recomended for rejection"),
            Q(forward_for_approval=True),

            approved=False
        )

        return render(request, self.template_name, context)


# Principle licence approval
decorators = [login_required(login_url='login'),allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class PrincipleLicenceAssign(UpdateView):

    model = PrincipleLicence
    fields = [
        'assigned_to_inspector',
        'manager_remarks',
        'date_assigned',
       
    ]

    template_name = 'administrator/approvers/principle/manager.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/admin'
    queryset = PrincipleLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):

        licence = form.save(commit=False)
        licence.date_assigned = timezone.now()
        licence.assigned = True
        licence.save()

        return redirect('administrator:verification_officer_home')


# Employee licence approval
decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class EmployeeLicenceAssign(UpdateView):

    model = EmployeeLicence
    fields = [
        'assigned_to_inspector',
        'manager_remarks',
        'date_assigned'

    ]

    template_name = 'administrator/approvers/employee/employee_manager.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/verification'
    queryset = EmployeeLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):

        licence = form.save(commit=False)

        licence.date_assigned = timezone.now()

        licence.save()
        return redirect('administrator:verification_officer_home')


# Premise licence approval
decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class PremiseLicenceAssign(UpdateView):

    model = PremiseLicence
    fields = [
        'assigned_to_inspector',
        'manager_remarks',
        'date_assigned'
    ]

    template_name = 'administrator/approvers/premise/premise_manager.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/admin'
    queryset = PremiseLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):

        licence = form.save(commit=False)

        licence.date_assigned = timezone.now()
        licence.assigned = True
        licence.save()
        return redirect('administrator:verification_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['inspector'])]


@method_decorator(decorators, 'dispatch')
class PrincipleInspectorsUpdate(UpdateView):
    model = PrincipleLicence
    fields = [
        'inspection_authority_status',
        'inspection_authority_remarks',
        'forward_for_verification',
        'inspection_report',
        'defer_to_inspector',

    ]

    template_name = 'administrator/approvers/principle/inspector.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/inspection'
    queryset = PrincipleLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):

        licence = form.save(commit=False)

        if licence.inspection_authority_status == "Recomended for a licence":

            licence.forward_for_verification = True
            licence.defer_to_inspector = False

            licence.save()

        elif licence.inspection_authority_status == "Recomended for rejection":

            licence.forward_for_verification = True
            licence.defer_to_inspector = False

            licence.save()

        else:
            licence.forward_for_verification = False
            licence.defer_to_inspector = False
            licence.save()

        # licence.updated_by = self.request.user
        # licence.updated_at = timezone.now()
        # licence.save()
        return redirect('administrator:inspecting_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class PrincipleVerifiersUpdate(UpdateView):
    model = PrincipleLicence
    fields = [
        'verification_authority_status',
        'verification_authority_remarks',
        'forward_for_approval',
        'defer_to_verifier',
        'defer_to_inspector',
        'forward_for_verification'
    ]

    template_name = 'administrator/approvers/principle/verifier.html'

    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/verification'
    queryset = PrincipleLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):
        licence = form.save(commit=False)

        if licence.verification_authority_status == "Recomended for approval":

            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.defer_to_inspector = False
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()

        elif licence.verification_authority_status == "Recomended for rejection":

            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.defer_to_inspector = False
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()
            
            licence.save()

        elif licence.verification_authority_status == "Defered":
            licence.forward_for_verification = False
            licence.forward_for_approval = False

            licence.defer_to_inspector = True
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()
            
            licence.save()
        
        else:

            pass

      
        return redirect('administrator:verification_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['approver'])]


@method_decorator(decorators, 'dispatch')
class PrincipleApproversUpdate(UpdateView):

    model = PrincipleLicence
    fields = [
        'approving_authority_status',
        'approving_authority_remarks',
        'approved',
        'defer_to_verifier',
        'forward_for_approval',

        'forward_for_verification',
        'defer_to_inspector',

    ]

    template_name = 'administrator/approvers/principle/approver.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/approval'
    queryset = PrincipleLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):
        licence = form.save(commit=False)

        if licence.approving_authority_status == "Defered":
            licence.forward_for_verification = True
            licence.defer_to_verifier = True
            licence.approved = False
            licence.forward_for_approval = False

            licence.approved_by = self.request.user
            licence.date_approved = timezone.now()
            licence.expiry_date = licence.date_applied.year + 1
            licence.save()
        else:
            licence.defer_to_verifier = False
            licence.approved = True
            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.approved_by = self.request.user
            licence.date_approved = timezone.now()
            licence.expiry_date = licence.date_applied.year + 1

            licence.save()
        return redirect('administrator:approving_officer_home')



decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['inspector'])]


@method_decorator(decorators, 'dispatch')
class EmployeeInspectorsUpdate(UpdateView):
    model = EmployeeLicence
    fields = [
        'inspection_authority_status',
        'inspection_authority_remarks',
        'forward_for_verification',
        'defer_to_inspector',

    ]

    template_name = 'administrator/approvers/employee/employee_inspector.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/inspection'
    queryset = EmployeeLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):

        licence = form.save(commit=False)

        if licence.inspection_authority_status == "Recomended for a licence":

            licence.forward_for_verification = True
            licence.defer_to_inspector = False

            licence.save()

        elif licence.inspection_authority_status == "Recomended for rejection":

            licence.forward_for_verification = True
            licence.defer_to_inspector = False
            licence.save()

        else:
            licence.forward_for_verification = False
            licence.defer_to_inspector = False
            licence.save()

        # licence.updated_by = self.request.user
        # licence.updated_at = timezone.now()
        # licence.save()
        return redirect('administrator:inspecting_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class EmployeeVerifiersUpdate(UpdateView):
    model = EmployeeLicence
    fields = [
        'verification_authority_status',
        'verification_authority_remarks',
        'forward_for_approval',
        'defer_to_verifier',
        'defer_to_inspector',
        'forward_for_verification'
    ]

    template_name = 'administrator/approvers/employee/employee_verifier.html'

    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/verification'
    queryset = EmployeeLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):
        licence = form.save(commit=False)

        if licence.verification_authority_status == "Recomended for approval":

            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.defer_to_inspector = False
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()

        elif licence.verification_authority_status == "Recomended for rejection":

            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.defer_to_inspector = False
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()

        elif licence.verification_authority_status == "Defered":
            licence.forward_for_verification = False
            licence.forward_for_approval = False

            licence.defer_to_inspector = True
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()
        else:
            pass

        # licence.updated_by = self.request.user
        # licence.updated_at = timezone.now()
        return redirect('administrator:verification_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['approver'])]


@method_decorator(decorators, 'dispatch')
class EmployeeApproversUpdate(UpdateView):

    model = EmployeeLicence
    fields = [
        'approving_authority_status',
        'approving_authority_remarks',
        'approved',
        'defer_to_verifier',
        'forward_for_approval',

        'forward_for_verification',
        'defer_to_inspector',

    ]

    template_name = 'administrator/approvers/employee/employee_approver.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/approval'
    queryset = EmployeeLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):
        licence = form.save(commit=False)

        if licence.approving_authority_status == "Defered":
            licence.forward_for_verification = True
            licence.defer_to_verifier = True
            licence.approved = False
            licence.forward_for_approval = False

            licence.approved_by = self.request.user
            licence.date_approved = timezone.now()
            licence.expiry_date = licence.date_applied.year + 1
            licence.save()
        else:
            licence.defer_to_verifier = False
            licence.approved = True
            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.approved_by = self.request.user
            licence.date_approved = timezone.now()
            licence.expiry_date = licence.date_applied.year + 1
            licence.save()
        return redirect('administrator:approving_officer_home')




decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['inspector'])]


@method_decorator(decorators, 'dispatch')
class PremiseInspectorsUpdate(UpdateView):
    
    model = PremiseLicence
    
    # fields = [
    #     'inspection_authority_status',
    #     'inspection_authority_remarks',
    #     'forward_for_verification',
    #     'inspection_report',
    #     'defer_to_inspector',
    # ]

    # general checklist 

    fields = [

        'inspection_authority_status',
        'inspection_authority_remarks',
        'forward_for_verification',
        'defer_to_inspector',

        'licence_availability', 
        'licence_availability_comments', 

        'licence_display', 
        'licence_display_comments', 
        
        'premises_surrounding_public_amenities', 
        'premises_urrounding_public_amenities_comments', 
        
        'convinience_facility', 
        'common_area', 
        'convenience_facilities_and_common_area_comments', 

        'size_of_premises',  
        'size_of_premises_comments', 
        
        'metal_detector', 
        'security_guard', 
        'access_restriction_and_security_comments',

        'television_set_positioning', 
        'television_set_positioning_comments', 
        
        'display_of_rules_on_betting_and_gaming', 
        'display_of_rules_on_betting_and_gaming_comments', 
        
        'display_of_board_notices_and_rules', 
        'display_of_board_notices_and_rules_comments', 
    
        'data_protection_policy', 
        'data_protection_policy_comments',

        'gaming_tables_number', 
        'slot_machines_number', 
        'fish_hunter_number', 
        'coin_machines_number', 

        # cassino and headoffice checklist 
        'plans_and_diagram_of_casino', 
        'plans_and_diagram_of_casino_comments', 

        'survillance_systems', 
        'survillance_systems_comments', 
        
        'counting_rooms_or_cages', 
        'counting_rooms_or_cages_comments', 
        
        'casino_and_gaming_rules', 
        'casino_and_gaming_rules_comments', 
        
        'communication_facilities', 
        'communication_facilities_comments', 
        
        'anti_money_laundering_policy', 
        'anti_money_laundering_policy_comments', 
    
   ]

    template_name = 'administrator/approvers/premise/premise_inspector.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/inspection'
    queryset = PremiseLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):

        licence = form.save(commit=False)

        if licence.inspection_authority_status == "Recomended for a licence":

            licence.forward_for_verification = True
            licence.defer_to_inspector = False

            licence.save()

        elif licence.inspection_authority_status == "Recomended for rejection":

            licence.forward_for_verification = True
            licence.defer_to_inspector = False
            licence.save()

        else:
            licence.forward_for_verification = False
            licence.defer_to_inspector = False
            licence.save()

        # licence.updated_by = self.request.user
        # licence.updated_at = timezone.now()
        # licence.save()
        return redirect('administrator:inspecting_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['verifier'])]


@method_decorator(decorators, 'dispatch')
class PremiseVerifiersUpdate(UpdateView):
    model = PremiseLicence
    fields = [
        'verification_authority_status',
        'verification_authority_remarks',
        'forward_for_approval',
        'defer_to_verifier',
        'defer_to_inspector',
        'forward_for_verification'
    ]

    template_name = 'administrator/approvers/premise/premise_verifier.html'

    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/verification'
    queryset = PremiseLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):
        licence = form.save(commit=False)

        if licence.verification_authority_status == "Recomended for approval":

            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.defer_to_inspector = False
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()

        elif licence.verification_authority_status == "Recomended for rejection":

            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.defer_to_inspector = False
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()

        elif licence.verification_authority_status == "Defered":
            licence.forward_for_verification = False
            licence.forward_for_approval = False

            licence.defer_to_inspector = True
            licence.defer_to_verifier = False

            licence.verified_by = self.request.user
            licence.date_verified = timezone.now()

            licence.save()
        else:
            pass

        # licence.updated_by = self.request.user
        # licence.updated_at = timezone.now()
        return redirect('administrator:verification_officer_home')


decorators = [login_required(login_url='login'),
              allowed_users(allowed_roles=['approver'])]


@method_decorator(decorators, 'dispatch')
class PremiseApproversUpdate(UpdateView):

    model = PremiseLicence
    fields = [
        'approving_authority_status',
        'approving_authority_remarks',
        'approved',
        'defer_to_verifier',
        'forward_for_approval',

        'forward_for_verification',
        'defer_to_inspector',

    ]

    template_name = 'administrator/approvers/premise/premise_approver.html'
    pk_url_kwarg = 'certificate_number'
    success_url = '/administrator/approval'
    queryset = PremiseLicence.objects.all()
    context_object_name = 'verified'

    def form_valid(self, form):
        licence = form.save(commit=False)

        if licence.approving_authority_status == "Defered":
            licence.forward_for_verification = True
            licence.defer_to_verifier = True
            licence.approved = False
            licence.forward_for_approval = False

            licence.approved_by = self.request.user
            licence.date_approved = timezone.now()
            # licence.expiry_date = licence.date_applied.year + 1 
            licence.save()
        else:
            licence.defer_to_verifier = False
            licence.approved = True
            licence.forward_for_verification = True
            licence.forward_for_approval = True

            licence.approved_by = self.request.user
            licence.date_approved = timezone.now()
            # licence.expiry_date = licence.date_applied.year + 1
            licence.save()
        return redirect('administrator:approving_officer_home')



decorators = [login_required(login_url='login'),allowed_users(allowed_roles=['verifier'])]
@method_decorator(decorators, 'dispatch')
class LicenceAssignmentView(View):
    template_name = 'administrator/assign/licence_assign.html' 

    def get(self, request):
        
        context = {}
        new_principle_licence_assignment = PrincipleLicence.objects.all()
        new_keyemployee_licence_assignment = EmployeeLicence.objects.all()
        new_premise_licence_assignment = PremiseLicence.objects.all()

        un_assigned_principle_licence = PrincipleLicence.objects.filter(
            assigned = False
        ).count()

        context['un_assigned_principle_licence'] = un_assigned_principle_licence

        context['new_principle_licence_assignment'] = new_principle_licence_assignment
        context['new_keyemployee_licence_assignment'] = new_keyemployee_licence_assignment
        context['new_premise_licence_assignment'] = new_premise_licence_assignment

        return render(request, self.template_name, context)




decorators = [login_required(login_url='login'),allowed_users(allowed_roles=['admin'])]
@method_decorator(decorators, 'dispatch')
class AdminOfficerView(View):
    # template_name = 'administrator/admin_home.html'

    template_name = 'administrator/admin_home_extended.html'

    def get(self, request):
        context = {}

        new_principle_licence_assignment = PrincipleLicence.objects.all()
        new_keyemployee_licence_assignment = EmployeeLicence.objects.all()
        new_premise_licence_assignment = PremiseLicence.objects.all()
        number_of_principle = len(PrincipleLicence.objects.all())
        number_of_employee = len(EmployeeLicence.objects.all())
        number_of_premise = len(PremiseLicence.objects.all())

        total = number_of_principle + number_of_employee + number_of_premise

        context['new_principle_licence_assignment'] = new_principle_licence_assignment
        context['new_keyemployee_licence_assignment'] = new_keyemployee_licence_assignment
        context['new_premise_licence_assignment'] = new_premise_licence_assignment
        context['number_of_principle'] = number_of_principle
        context['number_of_employee'] = number_of_employee
        context['number_of_premise'] = number_of_premise
        context['total'] = total

        return render(request, self.template_name, context)


