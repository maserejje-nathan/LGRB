from django.urls import path, include
from django.contrib.auth import views as auth_views 
from account.views import *
from django.views.decorators.csrf import csrf_exempt
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


temp_one = os.path.join(BASE_DIR, 'account/templates/account/password_reset_done.html')
temp_two = os.path.join(BASE_DIR, 'account/templates/account/password_reset_confirm.html')
temp_three = os.path.join(BASE_DIR, 'account/templates/account/password_reset_complete.html')



urlpatterns = [
    path('', auth_page, name="auth-page"),
    path('', enablejs, name="enablejs"),
    path('login/', client_login, name="login"),
    path('login/admin', admin_login, name="admin_login"),
    path('logout/', client_logout, name="logout"),
    path('logout/admin', admin_logout, name="admin_logout"),
    
    path('profile/', profile, name="profile"),
    
    # path('register/', csrf_exempt(RegisterView.as_view()), name="register"),
    path('register/', RegisterView.as_view(), name="register"),


    path('accounts/password_reset/', PasswordResetRequestView, name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name=temp_one), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name=temp_two), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name=temp_three), name='password_reset_complete'),


    path('accounts/token/ursb', ursb_token, name="ursb"),
    path('accounts/token/nira', nira_token, name="nira"),
    path('accounts/nira/credentials', nira_credentials_token, name="nira"),

    path('accounts/nira', nira, name="auth-nira"),
    path('accounts/ursb', ursb, name="auth-ursb"),
    
    path('accounts/ugpass/login', ugpass, name="ugpass"),
    path('daes_redirect/', redirect_page, name="daes_redirect"),


]