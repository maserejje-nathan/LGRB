from django.urls import path 
from django.contrib import admin
from administrator.views import *
from client.views import *
from reports.views import *

app_name = 'reports'

urlpatterns = [
    path('base/line/', PrintUsersPDF.as_view(), name="employee_revenue_op"),
    
    # revenue combined 
    path('principle/revenue/', PrincipleLicencerevenueView.as_view(), name="principle_revenue"),
    path('premise/revenue/', PremiseLicenceRevenueView.as_view(), name="premise_revenue"),
    path('employee/revenue/', EmployeeLicenceRevenueView.as_view(), name="employee_revenue"),

    # premise applcation
    path('premise/approvals', PremiseApprovalsView.as_view(), name="all_premise_approvals"),
    path('premises/all/', AllPremisesPdfReport.as_view(), name="all_premise_report"),

    # principle application 
    path('principle/approvals/', PrincipleApprovalsView.as_view(), name="all_principle_approvals"),
    path('principle/all', AllPrinciplePdfReport.as_view(), name="all_principle_report"),

    # employee approval 
    path('employee/approvals', EmployeeApprovalsView.as_view(), name="all_employees_approvals"),
    path('employee/all', AllEmployeesPdfReport.as_view(), name="all_employees_report"),
    path('employee/company', EmployeeByCompanyPdfReport.as_view(), name="employee_by_company"),
    path('emp/recomended', AllRecomenedEmployeesPdfReport.as_view(), name="recommended_employees"),


    path('employees/all', AllEmployees.as_view(), name="employees-all-op"),
    path('principle/all', AllPrincipleLicences.as_view(), name="principle-all-op"),

    path('principle/csv', AllPrincipleCsvReport.as_view(), name="principle-all-op"),




]