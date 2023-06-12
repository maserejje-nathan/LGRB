
from django.urls import path, include
from api.views import *



urlpatterns = [

    path('company/',CompanyListView.as_view(), name="company_list"),
    path('company/<int:brn>',CompanyByBrn.as_view(), name="company_list_by_brn"),

    
    path('Individual/',IndividualListView.as_view(), name="company_list"),
    path('Individual/<ppn>/<nin>',IndividualByWpnNin.as_view(), name="individual_list_byrn"),


    path('premise/', PremiseListView.as_view(), name="premise_list"),
    path('premise/company/<int:id>', PremiseListView.as_view(), name="premise_list"),


    path('employee/', EmployeeListView.as_view(), name="employee_list"),
    path('principle/', PrincipleListView.as_view(), name="principle_list"),
    

    # path('update/<int:certificateid>', CertificateUpdateView.as_view(), name="update-certificate"),
    # path('delete/<int:certificateid>', CertificateDeleteView.as_view(), name="delete-certificate"),
    # path('education/get', EducationListView.as_view(), name="view-education"),
    # path('document/add', CreateReport.as_view(), name="add-document"),
    # path('documents/get', GetReport.as_view(), name="get-documents"),
    # path('document/filter/<str:reportid>', GetReportById.as_view(), name="get-document-by-id"),
    # path('education/add', CreateEducation.as_view(), name="create-education"),
    # path('experience/add', CreateExperience.as_view(), name="add-experience")

]