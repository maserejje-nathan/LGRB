
from dataclasses import fields
from http.client import HTTPResponse
from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
from django.db.models.query import QuerySet
import requests

from new.models import *
from django.conf import settings
from django.db import transaction
from config.choices import *
from account.models import *

# from renew.models import *

class InspectorsForm(forms.ModelForm):
    class Meta:
        model = PrincipleLicence
        fields =  [
            'inspection_authority_status',
            'inspection_authority_remarks',
            'forward_for_verification',
            'inspection_report',
            'defer_to_inspector',
        ]
        # fields = "__all__"


class VerifiersForm(forms.ModelForm):
    class Meta:
        model = PrincipleLicence
        
        fields =  [
            'verification_authority_status',
            'verification_authority_remarks',
            'forward_for_approval',
            'defer_to_inspector',
            'defer_to_verifier',
            'forward_for_verification'
        ]


class ApproversForm(forms.ModelForm):
    class Meta:
        model = PrincipleLicence
        fields =  [
            'approving_authority_status',
            'approving_authority_remarks',
            'approved',

            'defer_to_verifier',
            'forward_for_approval',

            'forward_for_verification',
            'defer_to_inspector',
            
        ]

    def clean(self):
        cleaned_data = super().clean()
        certificate_no = cleaned_data.get('certificate_number')
        approving_authority_status = cleaned_data.get('approving_authority_status')
        approving_authority_remarks = cleaned_data.get('approving_authority_remarks')

        if not approving_authority_status:
            raise forms.ValidationError("This field can not be empty ")
        if not approving_authority_remarks:
            raise forms.ValidationError("This field can not be empty")

        return cleaned_data


class AdminsForm(forms.ModelForm):
    class Meta:
        model = PrincipleLicence
        fields =  [
            'assigned_to_inspector', 
            'manager_remarks',
            'assigned'
        ]
