from django.urls import path 
from django.contrib import admin
from administrator.views import *
from client.views import *

app_name = 'administrator'

admin.site.site_header  =  "eLicensing Administrator"  
admin.site.site_title  =  "eLicensing Administration"
admin.site.index_title  =  "eLicensing Administrator"


urlpatterns = [   
    
    path('administrator/inspection', InspectingAuthorityView.as_view(), name="inspecting_officer_home"),
    path('administrator/verification', VerificationAuthorityView.as_view(), name="verification_officer_home"),
    path('administrator/approval', ApprovingAuthorityView.as_view(), name="approving_officer_home"),
    path('administrator/admin', AdminOfficerView.as_view(), name="admin_home"),
    path('administrator/licence/assign', LicenceAssignmentView.as_view(), name="licence-assign"),


    path('administrator/users/companies', CompanyListView.as_view(), name="company"),
    path('administrator/users/details', CompanyDetailView.as_view(), name="company-detail"),

    path('administrator/users/individuals', IndividualListView.as_view(), name="client"),
    path('administrator/users/individuals', IndividualDetailView.as_view(), name="client-detail"),

    path('administrator/users/admins', AdminListView.as_view(), name="admin"),
    path('administrator/users/admin/detail', AdminDetailView.as_view(), name="admin-detail"),

    path('administrator/achives', Archives.as_view(), name="achive"),


    path('administrator/user/add', AdminRegisterView.as_view(), name="user-add" ),

    path('licence/task/list', NewLicenceTaskList.as_view(), name="new_licence_task"),

    path('licence/assignment/inspection', NewInspectionAssignment.as_view(), name="new_inspection_assignment"),
    

    path('licence/load/principle/manager/<str:certificate_number>', PrincipleLicenceAssign.as_view(), name="principle-new-assign"),
    path('licence/load/employee/manager/<str:certificate_number>', EmployeeLicenceAssign.as_view(), name="employee-new-assign"),
    path('licence/load/premise/manager/<str:certificate_number>', PremiseLicenceAssign.as_view(), name="premise-new-assign"),

    path('licence/load/principle/inspection/<str:certificate_number>', PrincipleInspectorsUpdate.as_view(), name="PrincipleInspectorsUpdate"),
    path('licence/load/principle/verification/<str:certificate_number>', PrincipleVerifiersUpdate.as_view(), name="PrincipleVerifiersUpdate"),
    path('licence/load/principle/approval/<str:certificate_number>', PrincipleApproversUpdate.as_view(), name="PrincipleApproversUpdate"),
   
   

    path('licence/load/employee/inspection/<str:certificate_number>', EmployeeInspectorsUpdate.as_view(), name="EmployeeInspectorsUpdate"),
    path('licence/load/employee/verification/<str:certificate_number>', EmployeeVerifiersUpdate.as_view(), name="EmployeeVerifiersUpdate"),
    path('licence/load/employee/approval/<str:certificate_number>', EmployeeApproversUpdate.as_view(), name="EmployeeApproversUpdate"),


    path('licence/load/premise/inspection/<str:certificate_number>', PremiseInspectorsUpdate.as_view(), name="PremiseInspectorsUpdate"),
    path('licence/load/premise/verification/<str:certificate_number>', PremiseVerifiersUpdate.as_view(), name="PremiseVerifiersUpdate"),
    path('licence/load/premise/approval/<str:certificate_number>', PremiseApproversUpdate.as_view(), name="PremiseApproversUpdate"),
    



    # path('principle/activity/', ApprovalReport.as_view(), name="principle-revenue"),
    # path('premise/activity/', PremiseLicenceRevenue.as_view(), name="premise-revenue"),
    # path('employee/activity/', EmployeeLicenceRevenue.as_view(), name="employee-revenue"),




]