from django.urls import path
from bankguarantee.views import *

app_name = 'bankguarantee'


urlpatterns = [
    path('bankguaranteee/new/create', BankGuaranteeCreate.as_view(), name="new_bank_guarantee_create" ),
    path('bankguaranteee/new/list', BankGuaranteeList.as_view(), name="new_bank_guarantee_list" ),
    path('bankguaranteee/new/detail', BankGuaranteeDetail.as_view(), name="_new_bank_guarantee_detail" ),
    path('bankguaranteee/new/update/<int:pk>/', BankGuaranteeUpdate.as_view(), name="new_bank_guarantee_update" ),

    path('bankguaranteee/renew/create', RenewedBankGuaranteeCreate.as_view(), name="renew_bank_guarantee_create" ),
    path('bankguaranteee/renew/list', RenewedBankGuaranteeList.as_view(), name="renew_bank_guarantee_list" ),
    path('bankguaranteee/renew/detail', RenewedBankGuaranteeDetail.as_view(), name="renew_bank_guarantee_detail" ),
    path('bankguaranteee/renew/update/<int:pk>/', RenewedBankGuaranteeUpdate.as_view(), name="renew_bank_guarantee_update" ),

]