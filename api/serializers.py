from rest_framework import serializers
from api.models import *
from new.models import *
from account.models import Account


class CompanySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Account
        # fields = '__all__'
        fields = [
            'legalStatus',
            'citizenship',
            'email',
            'first_name', 
            'last_name', 
            'brn',
            'phone_number'
        ]
        depth=1


class IndividualSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # fields = '__all__'
        fields = [
            'legalStatus',
            'citizenship',
            'email',
            'phone_number',
            'first_name', 
            'last_name', 
            'ppn',
            'nin',
        ]
        depth=1


class PrincipleLicenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrincipleLicence
        fields = '__all__'


class PremiseLicenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PremiseLicence
        fields = '__all__'
        # depth=1


class EmployeeLicenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeLicence
        fields = '__all__'


# class PractionerSerializer(serializers.ModelSerializer):
#     account = AccountSerializer(many=True, read_only=True)
#     educations = PremiseLicenceSerializer(many=True, read_only=True)
#     employee = EmployeeLicenceSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = "__all__"
#         # depth=1

        



        
