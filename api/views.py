
from django.http import Http404

from rest_framework import generics, permissions, status, renderers, exceptions
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from new.models import *
from api.serializers import *

class CompanyListView(generics.GenericAPIView):

    serializer_class = CompanySerializer

    def get(self,request, *args, **kwargs):
       
        practitioners = Account.objects.filter(
            Q(role = "client"),
            Q(legalStatus = "Company")
        )
       
        serializer = self.serializer_class(practitioners, many=True)
        return Response(serializer.data)


class CompanyByBrn(generics.GenericAPIView):
    serializer_class = CompanySerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brn']
    
    
    def get(self, request, brn):
        if request.method == "GET":

            try:
                company = Account.objects.get(brn=brn)
                serializer = self.serializer_class(company)  
                return Response({
                    "code": 200,
                    "company": serializer.data
                }, status=status.HTTP_200_OK)

            except Account.DoesNotExist:
                return Response({
                    "code":400,
                    "message": "Company does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)


class IndividualListView(generics.GenericAPIView):

    serializer_class = IndividualSerializer

    def get(self,request, *args, **kwargs):
       
        individuals = Account.objects.filter(
            Q(role = "client"),
            Q(legalStatus = "Individual")
        )
       
        serializer = self.serializer_class(individuals, many=True)
        return Response(serializer.data)


class IndividualByWpnNin(generics.GenericAPIView):

    serializer_class = IndividualSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nin', 'ppn']
   
    def get(self, request, nin, ppn):

        if request.method == "GET":
            
            try:
                query =  Q(nin=nin) | Q(ppn=ppn)
                company = Account.objects.filter(query)
                serializer = self.serializer_class(company, many=True)  # Note the 'many=True' for multiple objects
                return Response({
                    "code": 200,
                    "company": serializer.data
                }, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": "Company does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
class PrincipleListView(generics.GenericAPIView):

    serializer_class = EmployeeLicenceSerializer

    

    def get(self,request, *args, **kwargs):
       
        practitioners = PrincipleLicence.objects.all()
       
        serializer = self.serializer_class(practitioners, many=True)
        return Response(serializer.data)
    

class EmployeeListView(generics.GenericAPIView):

    serializer_class = EmployeeLicenceSerializer

    

    def get(self,request, *args, **kwargs):
       
        practitioners = EmployeeLicence.objects.all()
       
        serializer = self.serializer_class(practitioners, many=True)
        return Response(serializer.data)
    
    
class PremiseListView(generics.GenericAPIView):

    serializer_class = PremiseLicenceSerializer

 
    def get(self,request, *args, **kwargs):
       
        practitioners = PrincipleLicence.objects.all()
       
        serializer = self.serializer_class(practitioners, many=True)
        return Response(serializer.data)
    

'''    

class CertificateListView(generics.GenericAPIView):
    
    serializer_class = CertificateSerializer

    def get(self, request, *args, **kwargs):

        certificates = Certificate.objects.all()
       
        serializer = self.serializer_class(certificates, many=True)

        return Response(serializer.data)


class CreateCeritificateView(generics.GenericAPIView):

    serializer_class = CertificateSerializer

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code":201,
                    "message": "certificate applied succesffully"
                }, status = status.HTTP_201_CREATED)
            else:
                return Response({
                        "code": 400,
                        "message": "something went wrong",
                        "errors": serializer.errors
                       
                    },status = status.HTTP_400_BAD_REQUEST)
   

class CertificateUpdateView(generics.GenericAPIView):
    serializer_class = CertificateSerializer
    permission_classes  = [permissions.AllowAny]

    def get_object(self, certificateid, format=None):
        try:
            return Certificate.objects.get(certificateid=certificateid)
        except Certificate.DoesNotExist:
            raise Http404

    def put(self, request, certificateid, format=None):
        
        if request.method == "PUT":
            
            user = self.get_object(certificateid)

            serializer = self.serializer_class(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 206,
                    "message": "certificate updated successfully "
                }, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response({
                    "code": 400,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "code": 200,
            "message": serializer.data
        }, status= status.HTTP_200_OK)


class CertificateDeleteView(generics.GenericAPIView):
    serializer_class = CertificateSerializer
    permission_classes  = [permissions.AllowAny]

    def get_object(self, certificateid, format=None):
        try:
            return Certificate.objects.get(certificateid=certificateid)
        except Certificate.DoesNotExist:
            raise Http404


    def delete(self, request, certificateid, format=None):
        user = self.get_object(certificateid)
        user.delete()
        return Response({
            "code": 200,
            "message": "user successfully deleted"
        })

# education
class EducationListView(generics.GenericAPIView):
    serializer_class = EducationSerializer

    def get(self, request, *args, **kwargs):

        certificates = Education.objects.all()
       
        serializer = self.serializer_class(certificates, many=True)

        return Response(serializer.data)


class CreateEducation(generics.GenericAPIView):

    serializer_class = EducationSerializer
    renderer_classes = [renderers.JSONRenderer]


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 200, 
                "message": "education data added succesfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "code": 400,
                "message": "something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)


# experience
class CreateExperience(generics.GenericAPIView):
    serializer_class = ExperienceSerializer
    
    def post(self, request):
        if request.method == "POST":
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 200,
                    "message": "work experience added successfully"
                }, status=status.HTTP_201_CREATED)

            else:
                return Response({
                    "code": 200,
                    "message": "something has gone wrong! try again later"
                }, status=status.HTTP_400_BAD_REQUEST)


# document
class CreateReport(generics.GenericAPIView):

    serializer_class = ReportSerializer
    renderer_classes = [renderers.JSONRenderer]


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 201, 
                "message": "education data added succesfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "code": 400,
                "message": "something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)


class GetReport(generics.GenericAPIView):

    serializer_class = ReportSerializer

    def get(self, request):
        if request.method == "GET":

            reports = Report.objects.all()

            serializer = self.serializer_class(reports, many=True)

            return Response({
                "code": 200,
                "data": serializer.data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 400,
                "message": "something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)


class GetReportById(generics.GenericAPIView):
    
        
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reportid']
    
    
    def get(self, request, reportid):
        if request.method == "GET":

            try:
                report = Report.objects.get(reportid=reportid)
                serializer = self.serializer_class(report)  
                return Response({
                    "code": 200,
                    "report": serializer.data
                }, status=status.HTTP_200_OK)

            except Report.DoesNotExist:
                return Response({
                    "code":400,
                    "message": "report document does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)

       
'''
    