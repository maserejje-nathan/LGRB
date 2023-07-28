from django.contrib import admin
from new.models import *



# class PRNInline(admin.TabularInline):
#     model = PaymentRequestNumber
#     fk_name = 'license'

# class BankGuaranteeInline(admin.TabularInline):
#     model = BankGuarantee
#     fk_name = 'bank_guarantee'

# class LicenceAdmin(admin.ModelAdmin):
#     inlines = [PRNInline, BankGuaranteeInline]
    

# class BankGuaranteeAdmin(admin.ModelAdmin):
#     inlines = [BankGuaranteeInline]


admin.site.register(PrincipleLicence)
# admin.site.register(PrincipleLicence, LicenceAdmin)
admin.site.register(EmployeeLicence)
admin.site.register(PremiseLicence)




