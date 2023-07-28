from django.urls import path
from new.views import *

app_name = 'new'

urlpatterns = [

    # principle licence 
    path('licence/principlelicence', PrincipleLicenceCreate.as_view(), name="principle-apply"),
    path('licence/principe/detail/<int:id>', PrincipleLicenceDetail.as_view(), name="principle-detail"),
    path('licence/principe/update/<int:id>', PrincipleLicenceUpdate.as_view(), name="principle-update"),

    # employee licence 
    path('licence/employee-licence', EmployeeLicenceCreate.as_view(), name="key-employee-apply"),
    path('licence/employee/detail/<int:pk>', EmployeeLicenceDetail.as_view(), name="employee-detail"),
    path('licence/employee/update/<int:id>', EmployeeLicenceUpdate.as_view(), name="employee-update"),

    # premise licence
    path('premise/list', premise_list, name='premise_list'), 
    path('premise/create', create_premise, name='create_premise'),
    path('create/premise', CreatePremise.as_view(), name="create_premise"),
    path('premise/update/<int:id>', premise_update, name='premise_update'),
    path('premise/delete/<int:id>', premise_delete, name='premise_delete'),
    path('premise/count', get_premise_amount, name="add-premise-count"),
    path('premise/payments/list', PremisePaymentList.as_view(), name='premise_payment_list'),
    path('licence/premise/detail/<int:pk>', PremiseLicenceDetail.as_view(), name='premise-detail'),

    

    path('licence/premise/update/<int:id>', PremiseLicenceUpdate.as_view(), name="premise-update"),

    # prn 
    path('licence/prns', LicencePrns.as_view(), name="new_prn_list"),
    # employee 
    path('prn/pdf/employee/list/<int:pk>', new_employee_prn_pdf_view, name="new_employee_prn_pdf_view"),
    path('prn/pdf/employee/download/<int:pk>', new_employee_prn_pdf_download_view, name="new_employee_prn_pdf_download_view"),
    # principle
    # application fees
    path('prn/pdf/principle/list/<int:pk>', new_principle_prn_application_fee_pdf_view, name="new_principle_prn_pdf_view"),
    path('prn/pdf/principle/download/<int:pk>', new_principle_prn_application_fee_pdf_download_view, name="new_principle_prn_pdf_download_view"),
    # licence fees
    path('prn/pdf/lincefee/principle/list/<int:pk>', new_principle_prn_licence_fee_pdf_view, name="new_principle_prn_licence_fee_pdf_view"),
    path('prn/pdf/lincefee/principle/download/<int:pk>', new_principle_prn_licence_fee_pdf_download_view, name="new_principle_prn_licence_fee_pdf_download_view"),

    # premise
    path('prn/pdf/premise/list/<int:pk>', new_premise_prn_pdf_view, name="new_premise_prn_pdf_view"),
    path('prn/pdf/premise/download/<int:pk>', new_premise_prn_pdf_download_view, name="new_premise_prn_pdf_download_view"),
   
    # certificate 
    path('certificate/new', NewCertificateList.as_view(), name="new_certificate_list"),
    # employee 
    path('certificate/pdf/employee/list/<int:pk>', new_employee_certificate_pdf_view, name="new_employee_certificate_pdf_view"),
    path('certificate/pdf/employee/download/<int:pk>', new_employee_certificate_pdf_download_view, name="new_employee_certificate_pdf_download_view"),
    # principle
    path('certificate/pdf/principle/list/<int:pk>', new_principle_certificate_pdf_view, name="new_principle_certificate_pdf_view"),
    path('certificate/pdf/principle/download/<int:pk>', new_principle_certificate_pdf_download_view, name="new_principle_certificate_pdf_download_view"),
    # premise
    path('certificate/pdf/premise/list/<int:pk>', new_premise_certificate_pdf_view, name="new_premise_certificate_pdf_view"),
    path('certificate/pdf/premise/download/<int:pk>', new_premise_certificate_pdf_download_view, name="new_premise_certificate_pdf_download_view"),
    
    path('principlelicence/fee', get_principle_amount, name="get_principle_amount"),
    path('principlelicence/data', previous_principle_licence_data, name="previous_principle_licence_data"),
    path('employeelicence/data', previous_employee_licence_data, name="previous_employee_licence_data"),
    

    path('vr', check_premise_licence_fee_status, name="vr"),

    path('vrr', create_premise_licence_expiry_date, name="vrr"),

    path('pdf/<int:pk>/', view_pdf, name="pdf"),

    
]
