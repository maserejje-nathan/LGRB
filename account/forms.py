import logging
from xml.dom import ValidationErr
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from config.choices import legalStatus, citizenship, sex, roles_trimed

from account.models import Account
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
from django.contrib.auth.models import User

log = logging.getLogger(__name__)

from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationForm(UserCreationForm):

    legalStatus = forms.ChoiceField(label='Legal Status', required=False, choices=legalStatus,  widget=forms.Select(attrs={'class': 'form-control', 'name':'legalStatus', 'id':'legalStatus','type':'select'}))

    citizenship = forms.ChoiceField(label='Citizenship', required=False, choices=citizenship, widget=forms.Select(attrs={'class': 'form-control', 'name':'citizenship', 'id':'citizenship','type':'select'}))
    
    email = forms.EmailField(label='Email Address',   widget=forms.EmailInput(attrs={'class': 'form-control', 'name':'emailAddress', 'id':'email','type':'email', 'placeholder':'eg info@nita.go.ug '}))
    
    nin = forms.CharField(label='National Identification Number (NIN)', required=False, min_length=14,  max_length=14, widget=forms.TextInput(attrs={ 'class': 'form-control',  'name':'nin', 'id':'nin','type':'text', 'placeholder':'National Identification Number ','maxlength':'14'}))

    wpn = forms.CharField(label='Work Permit Number (WPN)', required=False, min_length=14,  max_length=14, widget=forms.TextInput(attrs={'class': 'form-control',  'name':'wpn', 'id':'wpn','type':'text', 'placeholder':'Work Permit Number ','maxlength':'14'}))

    ppn = forms.CharField(label='Passport Number (PPN)', required=False, min_length=14,  max_length=14, widget=forms.TextInput(attrs={'class': 'form-control',  'name':'ppn', 'id':'ppn','type':'text', 'placeholder':'Passport Number','maxlength':'14' }))

    card_number = forms.CharField(label='Card Number', required=False, min_length=9,  max_length=9, widget=forms.TextInput(attrs={'class': 'form-control',  'name':'card_number', 'id':'card_number','type':'text', 'placeholder':'Card Number','maxlength':'9' }))
           
    
    first_name = forms.CharField(label='Surname', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'first_name', 'id':'first_name','type':'text'}))

    last_name = forms.CharField(label='Given Names',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'last_name', 'id':'last_name','type':'text'}))

    phone_number = forms.CharField(min_length=10,  max_length=15, error_messages={'required': 'A valid phone number is required'}, help_text='If in another country, specify the country code e.g. +254', widget=forms.TextInput(attrs={'class': 'form-control', 'name':'phone_number', 'id':'phone_number','type':'text', 'placeholder':'eg: 0789098975'}))
    
    address = forms.CharField(label='Address',  required=False, max_length=50, widget=forms.TextInput(attrs={ 'class': 'form-control', 'name':'address', 'id':'address','type':'text', 'placeholder':'eg: address' }))
    
    sex = forms.ChoiceField(label='Sex',  choices=sex, required=False, widget=forms.Select(attrs={'class': 'form-control', 'name':'sex', 'id':'sex','type':'select'}))

    # businees data
    brn = forms.CharField(label='Business Registeration Number (BRN)',  required=False, max_length=14, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'brn', 'id':'brn','type':'text', 'placeholder':'Business Registration Number','maxlength':'14'}))
    busines_name = forms.CharField(label='Business Name',required=False,   widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'busines_name', 'id':'busines_name','type':'text'}))
    business_type = forms.CharField(label='Business Type',required=False,   widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'business_type', 'id':'business_type','type':'text'}))
    business_registration_date = forms.CharField(label='Registration Date', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'business_registration_date', 'id':'business_registration_date','type':'text'}))
    
    password1 = forms.CharField(max_length=254, label='Password',   widget=forms.PasswordInput(attrs={'class': 'form-control', 'name':'password1', 'id':'password1','type':'password', 'placeholder':'password','maxlength':'22',  'minlength':'8'}))
    password2 = forms.CharField(max_length=254, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'name':'password2', 'id':'password2','type':'password', 'placeholder':'confirm password','maxlength':'22',  'minlength':'8'}))


    class Meta:
        model = Account
        fields = [
            'legalStatus',
            'citizenship',
            'nin',
            'brn',
            'busines_name',
            'business_type',
            'business_registration_date',
            'wpn',
            'ppn',
            'email',
            'sex',
            'address',
            'phone_number', 
            'password1',
            'password2',
            'first_name',
            'last_name',

            'District', 
            'County',
            'Subcounty',
            'Parish',
            'Village',

        ]


class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class': 'form-control ', 'name':'email', 'id':'email','type':'email'}) )
    first_name = forms.CharField(label='First Name', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'first_name', 'id':'first_name','type':'text'}))
    last_name = forms.CharField(label='Last Name',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'last_name', 'id':'last_name','type':'text'}))
    role = forms.ChoiceField(label='Admin Role', required=False, choices=roles_trimed, widget=forms.Select(attrs={'class': 'form-control', 'name':'role', 'id':'role','type':'select'}))

    phone_number = forms.CharField(min_length=10,  max_length=15, error_messages={'required': 'A valid phone number is required'}, help_text='If in another country, specify the country code e.g. +254', widget=forms.TextInput(attrs={'class': 'form-control', 'name':'phone_number', 'id':'phone_number','type':'text', 'placeholder':'eg: 0789098975'}))    
    password1 = forms.CharField(max_length=254, label='Password',   widget=forms.PasswordInput(attrs={'class': 'form-control', 'name':'password1', 'id':'password1','type':'password', 'placeholder':'password','maxlength':'22',  'minlength':'8'}))
    password2 = forms.CharField(max_length=254, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'name':'password2', 'id':'password2','type':'password', 'placeholder':'confirm password','maxlength':'22',  'minlength':'8'}))

    class Meta:
        model = Account
        fields = ('first_name','last_name', 'phone_number', 'email', 'password1', 'password2','role')

    def clean(self):
        cleaned_data = super(AdminRegistrationForm, self).clean()
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords didnt match")
        phone  = cleaned_data.get('phone_number')
        if Account.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("Sorry this phone number is already in use")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("The user with this email exists")
        return cleaned_data


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', help_text='We will communicate to you via email', widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    full_names = forms.CharField(label='Organization Name', widget=forms.TextInput( attrs={'placeholder': 'e.g. National IT Authority - Uganda'}))
    phone_number = forms.CharField(min_length=10, max_length=15, error_messages={ 'required': 'A valid phone number is required'}, help_text='If in another country, specify the country code e.g. +254', widget=forms.TextInput(attrs={'placeholder': '0772123456'}))
    address = forms.CharField(label='Physical Address', widget=forms.TextInput( attrs={'placeholder': 'e.g. Mackinon Road, Plot 4, Kampala-Uganda'}))

    # location 
    District = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'District', 'id':'District','type':'text'}))
    County = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'County', 'id':'County','type':'text'}))
    Subcounty = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'Subcounty', 'id':'Subcounty','type':'text'}))
    Parish =  forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'Parish', 'id':'Parish','type':'text'}))
    Village = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'village', 'id':'village','type':'text'}))


    class Meta:
        model = Account
        fields = ('full_names', 'address', 'phone_number', 'image', 'email',  'District',
            'County',
            'Subcounty',
            'Parish',
            'Village',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(phone_number=phone_number)
        except Account.DoesNotExist:
            return phone_number
        raise forms.ValidationError(
            'Phone number "%s" is already in use.' % account)

    layout = Layout('full_names', 'address', 'phone_number', 'image', 'email')


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control ', 'name':'email', 'id':'email','type':'email'}))
    password = forms.CharField(max_length=254, label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control ', 'name':'password', 'id':'password','type':'password'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

    layout = Layout('email', 'password')
