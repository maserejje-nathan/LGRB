from account.models import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin




class AccountAdministrator(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'phone_number', 'address', 'role', 'date_joined', 'last_login', 'image', 'is_admin',
        'is_staff')
    search_fields = ('email', 'first_name', 'last_name',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('first_name', 'last_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'role', 'image')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Contact info', {'fields': ('phone_number', 'address')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'is_manager', 'is_director')}),
    )
    add_fieldsets = ((None, {'fields': ('email', 'password1', 'password2')}),
                     ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'role', 'image')}),
                     ('Contact info', {'fields': ('phone_number', 'address')}),
                     ('Permissions',
                      {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'is_manager', 'is_director')}))


admin.site.register(Account )
