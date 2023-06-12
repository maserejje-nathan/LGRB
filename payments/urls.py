from django.urls import path
from payments.views import *

app_name = 'payments'

urlpatterns = [
    
    path('payments/premise/list', ListPremisesPayments.as_view(), name="premise_licence_payment_list"), 
    path('payments/premise/client/list', ClientPremisesPaymentsList.as_view(), name="client_premise_payment_list"), 
    path('payment/premise/applicationfee', PremisesPayment.as_view(), name="payment-premise"),
    
    # payments 
    path('payment/old/fee/', LicenceFeePayments.as_view(), name="create_payment" ),
    path('payment/application/fee', ApplicationFeePayment.as_view(), name="application_fee_payment"),
    path('payment/licence/fee', LicenceFeePayment.as_view(), name="licence_fee_payment"),

    # ura endpoints
    path('accounts/prn/status', checkClearanceStatus, name="checkClearanceStatus"),
    path('accounts/tin/verify', verify_tin, name="verify_tin"), 
    path('accounts/token/ura', ura_token, name="ura"),
    path('accounts/prn/get/licence-fee', get_prn_licence_fee, name="get_prn_licence_fee"),
    path('accounts/prn/get/application-fee', get_prn_application_fee, name="get_prn_application_fee"), 
    path('accounts/prn/get/inspection-fee', get_prn_inspection_fee, name="get_prn_inspection_fee"), 
    path('api/data/bankguarantee/', get_new_bank_guarantee_data, name="get_new_bank_guarantee_data" ),
    path('premise/download/pdf', premise_pdf_download, name="premise_pdf_download" ),
    
]