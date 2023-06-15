from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.utils import timezone

import random
import threading
import datetime
import string
import pytz


# from dateutil import relativedelta

def upload_location(instance, filename):
    file_path = 'media/{filename}'.format(filename=filename)
    return file_path


def uploaded_location(instance, filename):
    file_path = 'media/username/{username}/{id}-{filename}'.format(
        name=str(instance.username).split()[0], id=str(instance.id), filename=filename)
    return file_path


def current_time():
    return pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now(), is_dst=None)


# def calculate_tomorrow(date):
#     return date + relativedelta.relativedelta(days=1)


# def calculate_three_days(date):
#     return date + relativedelta.relativedelta(days=3)


# def calculate_next_month(date):
#     return date + relativedelta.relativedelta(months=1)


# def calculate_next_week(date):
#     return date + relativedelta.relativedelta(weeks=1)

def calculate_one_years_time(date):
    return date - datetime.timedelta(days=360)


def calculate_start_day_of_month(date):
    # first_day = date.replace(day=1)
    # return (date - datetime.timedelta(days=datetime.date.today().weekday() % 7)).date()
    return date - datetime.timedelta(days=60)


def calculate_next_week_day(day_now):
    if day_now.isoweekday() == 5:
        day_now += datetime.timedelta(days=3)
    elif day_now.isoweekday() == 6:
        day_now += datetime.timedelta(days=2)
    else:
        day_now += datetime.timedelta(days=1)
    return day_now


def calculate_next_week_2_day(day_now):
    if day_now.isoweekday() == 5:
        day_now += datetime.timedelta(days=4)
    elif day_now.isoweekday() == 6:
        day_now += datetime.timedelta(days=3)
    else:
        day_now += datetime.timedelta(days=2)
    return day_now


def localize_date(date):
    return pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now(), is_dst=None)


def format_activity_time(date):
    date = timezone.localtime(date)
    if date.date() == datetime.date.today():
        return "at {}".format(date.strftime('%I:%M %p'))
    else:
        return "{} on {}".format(date.strftime('%I:%M %p'), date.strftime('%d %B'), )


def reference_code(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


def user_full_names(user):
    first_name = ""
    if user:
        first_name = "{} {}".format(user.first_name, user.last_name).title()
    return first_name


def get_base_url(request):
    if request.is_secure():
        return 'https://' + str(request.get_host())
    else:
        return 'http://' + str(request.get_host())


def certificate_generator(prefix):
    pk = random.randint(0, 99999)
    new_pk = int(pk) + 1

    existing_pks = ""
    final_pk = prefix + str(new_pk)
    return final_pk


def employee_licence_certificate_number(prefix):
    pk = random.randint(0, 99999)
    new_pk = int(pk) + 1

    existing_pks = ""
    final_pk = prefix + str(new_pk)
    return final_pk


def generate_and_send_otp(email):
    otp = random.randint(10000, 99999)
    subject = "One Time Password"
    email_body = f"Yor OTP is {otp}, use this to verify your email"
    email_sent = ""
    send_mail(subject, email_body, email_sent, [email])
    user = "Daniel okot"
    # user = .objects.get( email = email)
    user.otp = otp
    user.save()


def normalize_status(status):
    if status == "Reject":
        status = "Rejected"
    elif status == "Defer":
        status = "Deferred"
    elif status == "Approve":
        status = "Approved"
    elif status == "Recommend":
        status = "Recommended"
    return status


def user_actions(request, model, status, timestamp, comments):
    model.status = status
    # if status == 'Rejected':
    #     model.deferred_by = request.user
    #     model.date_rejected = timestamp

    # elif status == 'Deferred':
    #     model.rejected_by = request.user
    #     model.date_rejected = timestamp

    if request.user.role == "inspector":
        model.inspected_by = request.user
        model.date_inspected = timestamp
        # model.manager_comments = comments
        # model.manager_status = status
        # inspection_authority_status
        # inspection_authority_remarks

    if request.user.role == "verifier":
        # verification_authority_status 
        # verification_authority_remarks

        model.verified_by = request.user
        model.date_verified = timestamp
        # model.manager_comments = comments
        # model.manager_status = status

    if request.user.role == "approver":
        model.approving_authority_status = status
        model.approving_authority_remarks = comments
        # model.approved = True

        model.approved_by = request.user
        model.date_approved = timestamp
        # model.manager_comments = comments
        # model.manager_status = status

    # elif request.user.is_director:
    #     model.director_actioned = request.user
    #     model.date_director_responded = timestamp
    #     model.director_comments = comments
    #     model.director_status = status
    #     if status == 'Approved':
    #         model.approved_by = request.user
    #         model.date_approved = timestamp
    return model


def user_action(request, licence, status, timestamp, comments):
    licence.status = status
    if status == 'Rejected':
        licence.deferred_by = request.user
        licence.date_rejected = timestamp

    elif status == 'Deferred':
        licence.rejected_by = request.user
        licence.date_rejected = timestamp

    # user role based 

    if request.user.role == "inspector":
        licence.manager_actioned = request.user
        licence.date_manager_responded = timestamp
        licence.manager_comments = comments
        licence.manager_status = status

    elif request.user.role == "verifier":
        licence.director_actioned = request.user
        licence.date_director_responded = timestamp
        licence.director_comments = comments
        licence.director_status = status
        if status == 'Approved':
            licence.approved_by = request.user
            licence.date_approved = timestamp
    return licence

# inspecting officer
# inspection_authority_status =
# inspection_authority_remarks =
# date_inspected = 
# forward_for_verification =
# inspected_by = 
# evaluation_checklist  = 

# # verification officer
# verification_authority_status = 
# verification_authority_remarks =
# verified_by = 
# forward_for_approval = 
# date_verified = 

# # approving officer 
# approving_authority_status = 
# approved_by = 
# approving_authority_remarks
# approved = 
# date_approved = 

# # manager  
# assigned_to_inspector =
# assigned_to_verifier =
# manager_remarks = 
# date_assigned =
