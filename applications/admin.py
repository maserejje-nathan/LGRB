from django.contrib import admin
from applications.models import *


admin.site.register(PrincipleLicence)
# admin.site.register(PrincipleLicence, LicenceAdmin)
admin.site.register(EmployeeLicence)
admin.site.register(PremiseLicence)




