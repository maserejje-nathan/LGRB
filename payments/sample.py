
from new.models import PrincipleLicence
from payments.models import LicenceFeePayments


def update_pllf_payment_status():
    """
    Query the latest 3 records where the payment_status_id has not been updated
    """
    # principle_licence_fee
    licenses = PrincipleLicence.objects.filter( Q(principle_licence_fee__isnull=True) | Q(principle_licence_fee__iexact='')).order_by('-date_created')[:3]
    
    if licenses:
        for license in licenses:
            # query the payment table to get the response.
            payment = LicenceFeePayments.objects.all()
            
            # response = check_clearance_status(license.Prn)  # returns URA API response
            # if 'CheckPRNStatusResult' in response and 'StatusCode' in response['CheckPRNStatusResult'] and 'StatusDesc' in response['CheckPRNStatusResult']:
                # license.principle_licence_feeid = response['CheckPRNStatusResult']['StatusCode'] # you can retrieve any records you want from the API
            license.principle_licence_fee = payment.paymentid # you can retrieve any records you want from the API
            
            license.save()  # save to database
