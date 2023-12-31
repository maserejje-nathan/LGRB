# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BankGuarantee(models.Model):
    principle_licence_certificate_number = models.CharField(max_length=50)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=30, blank=True, null=True)
    bank = models.CharField(max_length=70, blank=True, null=True)
    bank_guarantee = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateField()
    verification_authority_status = models.CharField(max_length=30, blank=True, null=True)
    date_verified = models.DateTimeField(blank=True, null=True)
    approving_authority_status = models.CharField(max_length=30, blank=True, null=True)
    verification_authority_remarks = models.TextField(blank=True, null=True)
    approved = models.BooleanField()
    approving_authority_remarks = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bank Guarantee '


class EmployeeLicence(models.Model):
    purpose_of_application = models.CharField(max_length=10, blank=True, null=True)
    refrence_number = models.CharField(max_length=30, blank=True, null=True)
    licence_number = models.CharField(max_length=30, blank=True, null=True)
    previous_licence_number = models.CharField(max_length=30, blank=True, null=True)
    licence_type = models.CharField(max_length=200, blank=True, null=True)
    name_of_the_company = models.CharField(max_length=80, blank=True, null=True)
    name_of_the_employee = models.CharField(max_length=80, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    mobile_phone = models.IntegerField(blank=True, null=True)
    office_phone = models.IntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    work_permit = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    occupation = models.CharField(max_length=200, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    professional_membership = models.CharField(max_length=30, blank=True, null=True)
    interpoal_clearance = models.CharField(max_length=100)
    cv = models.CharField(max_length=100)
    application_fee = models.IntegerField(blank=True, null=True)
    previous_business_engagement = models.CharField(max_length=20, blank=True, null=True)
    name_of_the_employer = models.CharField(max_length=20, blank=True, null=True)
    crime_engagement = models.CharField(max_length=30, blank=True, null=True)
    crime_details = models.CharField(max_length=30, blank=True, null=True)
    generate_prn = models.BooleanField()
    tin = models.IntegerField(blank=True, null=True)
    prn = models.IntegerField(blank=True, null=True)
    error_code = models.CharField(max_length=30, blank=True, null=True)
    error_desc = models.CharField(max_length=30, blank=True, null=True)
    search_code = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    payment_expiry_date = models.CharField(max_length=30, blank=True, null=True)
    payment_registered_on = models.CharField(max_length=30, blank=True, null=True)
    payment_made_by = models.CharField(max_length=30, blank=True, null=True)
    payment_made_on = models.CharField(max_length=30, blank=True, null=True)
    ura_district = models.CharField(max_length=50, blank=True, null=True)
    ura_county = models.CharField(max_length=50, blank=True, null=True)
    ura_subcounty = models.CharField(max_length=50, blank=True, null=True)
    ura_village = models.CharField(max_length=50, blank=True, null=True)
    manager_remarks = models.TextField(blank=True, null=True)
    date_assigned = models.DateField(blank=True, null=True)
    assigned = models.BooleanField()
    inspection_authority_status = models.CharField(max_length=30, blank=True, null=True)
    inspection_authority_remarks = models.TextField(blank=True, null=True)
    forward_for_verification = models.BooleanField()
    date_inspected = models.DateTimeField(blank=True, null=True)
    defer_to_inspector = models.BooleanField()
    verification_authority_status = models.CharField(max_length=30, blank=True, null=True)
    verification_authority_remarks = models.TextField(blank=True, null=True)
    forward_for_approval = models.BooleanField()
    date_verified = models.DateTimeField(blank=True, null=True)
    defer_to_verifier = models.BooleanField()
    approving_authority_status = models.CharField(max_length=30, blank=True, null=True)
    approving_authority_remarks = models.TextField(blank=True, null=True)
    approved = models.BooleanField()
    date_approved = models.DateField(blank=True, null=True)
    date_applied = models.DateField(blank=True, null=True)
    expiry_date = models.CharField(max_length=30, blank=True, null=True)
    applicant = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    approved_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    assigned_to_inspector = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    inspected_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    verified_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    validity = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee Licence'


class EmployeeLicenceRenewal(models.Model):
    previous_licence_certificate = models.CharField(max_length=100)
    previous_licence_certificate_number = models.CharField(max_length=14, blank=True, null=True)
    type = models.CharField(db_column='Type', max_length=200, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=80, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mobile_phone = models.IntegerField(db_column='Mobile_phone', blank=True, null=True)  # Field name made lowercase.
    office_phone = models.IntegerField(db_column='Office_phone', blank=True, null=True)  # Field name made lowercase.
    postal_code = models.CharField(db_column='Postal_code', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=200, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=200, blank=True, null=True)  # Field name made lowercase.
    occupation = models.CharField(db_column='Occupation', max_length=200, blank=True, null=True)  # Field name made lowercase.
    qualification = models.CharField(db_column='Qualification', max_length=200, blank=True, null=True)  # Field name made lowercase.
    professional_membership = models.CharField(db_column='Professional_membership', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fee = models.IntegerField(blank=True, null=True)
    tin = models.IntegerField(blank=True, null=True)
    previous_engagement = models.CharField(db_column='Previous_Engagement', max_length=20, blank=True, null=True)  # Field name made lowercase.
    employer_name = models.CharField(db_column='Employer_name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    crime_history = models.CharField(db_column='Crime_History', max_length=30, blank=True, null=True)  # Field name made lowercase.
    crime_details = models.CharField(db_column='Crime_Details', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cv = models.CharField(db_column='Cv', max_length=100)  # Field name made lowercase.
    interpoal_clearance = models.CharField(db_column='Interpoal_clearance', max_length=100)  # Field name made lowercase.
    gernerate_prn = models.BooleanField()
    prn = models.IntegerField(blank=True, null=True)
    error_code = models.CharField(max_length=30, blank=True, null=True)
    error_desc = models.CharField(max_length=30, blank=True, null=True)
    expiry_date = models.CharField(max_length=30, blank=True, null=True)
    search_code = models.CharField(max_length=30, blank=True, null=True)
    date_created = models.DateField()
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    approving_authority = models.CharField(max_length=30, blank=True, null=True)
    date_approved = models.DateField(blank=True, null=True)
    license_issued = models.BooleanField()
    approved = models.BooleanField()
    email = models.CharField(max_length=50, blank=True, null=True)
    applicant = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    approved_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee Licence Renewal'


class PremiseLicenceTable(models.Model):
    operator_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    trade_name = models.CharField(max_length=30, blank=True, null=True)
    premise_name = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    town_council = models.CharField(max_length=200, blank=True, null=True)
    plot_number = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)
    equipment_in_the_premise = models.CharField(max_length=200, blank=True, null=True)
    number_of_gaming_devices = models.CharField(max_length=200, blank=True, null=True)
    inspection_fee = models.IntegerField(blank=True, null=True)
    signature = models.CharField(max_length=100, blank=True, null=True)
    generate_prn = models.BooleanField()
    tin = models.IntegerField(blank=True, null=True)
    prn = models.IntegerField(blank=True, null=True)
    error_code = models.CharField(max_length=30, blank=True, null=True)
    error_desc = models.CharField(max_length=30, blank=True, null=True)
    search_code = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    payment_expiry_date = models.CharField(max_length=30, blank=True, null=True)
    payment_registered_on = models.CharField(max_length=30, blank=True, null=True)
    payment_made_by = models.CharField(max_length=30, blank=True, null=True)
    payment_made_on = models.CharField(max_length=30, blank=True, null=True)
    ura_district = models.CharField(max_length=50, blank=True, null=True)
    ura_county = models.CharField(max_length=50, blank=True, null=True)
    ura_subcounty = models.CharField(max_length=50, blank=True, null=True)
    ura_village = models.CharField(max_length=50, blank=True, null=True)
    manager_remarks = models.TextField(blank=True, null=True)
    assigned = models.BooleanField()
    date_assigned = models.DateField(blank=True, null=True)
    inspection_authority_status = models.CharField(max_length=30, blank=True, null=True)
    inspection_authority_remarks = models.TextField(blank=True, null=True)
    forward_for_verification = models.BooleanField()
    date_inspected = models.DateTimeField(blank=True, null=True)
    inspection_report = models.CharField(max_length=100, blank=True, null=True)
    defer_to_inspector = models.BooleanField()
    verification_authority_status = models.CharField(max_length=30, blank=True, null=True)
    verification_authority_remarks = models.TextField(blank=True, null=True)
    forward_for_approval = models.BooleanField()
    date_verified = models.DateTimeField(blank=True, null=True)
    defer_to_verifier = models.BooleanField()
    approving_authority_status = models.CharField(max_length=30, blank=True, null=True)
    approving_authority_remarks = models.TextField(blank=True, null=True)
    approved = models.BooleanField()
    date_approved = models.DateField(blank=True, null=True)
    licence_availability = models.CharField(max_length=30, blank=True, null=True)
    licence_availability_comments = models.CharField(max_length=30, blank=True, null=True)
    licence_display = models.CharField(max_length=30, blank=True, null=True)
    licence_display_comments = models.CharField(max_length=30, blank=True, null=True)
    premises_surrounding_public_amenities = models.CharField(max_length=30, blank=True, null=True)
    premises_urrounding_public_amenities_comments = models.CharField(max_length=30, blank=True, null=True)
    convinience_facility = models.CharField(max_length=30, blank=True, null=True)
    common_area = models.CharField(max_length=30, blank=True, null=True)
    convenience_facilities_and_common_area_comments = models.CharField(max_length=30, blank=True, null=True)
    size_of_premises = models.CharField(max_length=30, blank=True, null=True)
    size_of_premises_comments = models.CharField(max_length=30, blank=True, null=True)
    metal_detector = models.CharField(max_length=30, blank=True, null=True)
    security_guard = models.CharField(max_length=30, blank=True, null=True)
    access_restriction_and_security_comments = models.CharField(max_length=30, blank=True, null=True)
    television_set_positioning = models.CharField(max_length=30, blank=True, null=True)
    television_set_positioning_comments = models.CharField(max_length=30, blank=True, null=True)
    display_of_rules_on_betting_and_gaming = models.CharField(max_length=30, blank=True, null=True)
    display_of_rules_on_betting_and_gaming_comments = models.CharField(max_length=30, blank=True, null=True)
    display_of_board_notices_and_rules = models.CharField(max_length=30, blank=True, null=True)
    display_of_board_notices_and_rules_comments = models.CharField(max_length=30, blank=True, null=True)
    data_protection_policy = models.CharField(max_length=30, blank=True, null=True)
    data_protection_policy_comments = models.CharField(max_length=30, blank=True, null=True)
    gaming_tables_number = models.CharField(max_length=30, blank=True, null=True)
    slot_machines_number = models.CharField(max_length=30, blank=True, null=True)
    fish_hunter_number = models.CharField(max_length=30, blank=True, null=True)
    coin_machines_number = models.CharField(max_length=30, blank=True, null=True)
    plans_and_diagram_of_casino = models.CharField(max_length=30, blank=True, null=True)
    plans_and_diagram_of_casino_comments = models.CharField(max_length=30, blank=True, null=True)
    survillance_systems = models.CharField(max_length=30, blank=True, null=True)
    survillance_systems_comments = models.CharField(max_length=30, blank=True, null=True)
    counting_rooms_or_cages = models.CharField(max_length=30, blank=True, null=True)
    counting_rooms_or_cages_comments = models.CharField(max_length=30, blank=True, null=True)
    casino_and_gaming_rules = models.CharField(max_length=30, blank=True, null=True)
    casino_and_gaming_rules_comments = models.CharField(max_length=30, blank=True, null=True)
    communication_facilities = models.CharField(max_length=30, blank=True, null=True)
    communication_facilities_comments = models.CharField(max_length=30, blank=True, null=True)
    anti_money_laundering_policy = models.CharField(max_length=30, blank=True, null=True)
    anti_money_laundering_policy_comments = models.CharField(max_length=30, blank=True, null=True)
    casino_games = models.CharField(max_length=30, blank=True, null=True)
    slot_machines = models.CharField(max_length=30, blank=True, null=True)
    genera_betting_and_virtual_machines = models.CharField(max_length=30, blank=True, null=True)
    pool_betting = models.CharField(max_length=30, blank=True, null=True)
    bingo_betting = models.CharField(max_length=30, blank=True, null=True)
    date_applied = models.DateField(blank=True, null=True)
    expiry_date = models.CharField(max_length=30, blank=True, null=True)
    applicant = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    approved_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    assigned_to_inspector = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    inspected_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    verified_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    validity = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Premise Licence Table'


class PremisePaymentTable(models.Model):
    licence_type = models.CharField(max_length=200, blank=True, null=True)
    name_of_the_company = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    premise = models.CharField(max_length=100, blank=True, null=True)
    licence_fee = models.IntegerField(blank=True, null=True)
    number_of_premises = models.IntegerField(blank=True, null=True)
    date_applied = models.DateField(blank=True, null=True)
    generate_prn = models.BooleanField()
    tin = models.IntegerField(blank=True, null=True)
    prn = models.IntegerField(blank=True, null=True)
    error_code = models.CharField(max_length=30, blank=True, null=True)
    error_desc = models.CharField(max_length=30, blank=True, null=True)
    search_code = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    payment_expiry_date = models.CharField(max_length=30, blank=True, null=True)
    payment_registered_on = models.CharField(max_length=30, blank=True, null=True)
    payment_made_by = models.CharField(max_length=30, blank=True, null=True)
    payment_made_on = models.CharField(max_length=30, blank=True, null=True)
    ura_district = models.CharField(max_length=50, blank=True, null=True)
    ura_county = models.CharField(max_length=50, blank=True, null=True)
    ura_subcounty = models.CharField(max_length=50, blank=True, null=True)
    ura_village = models.CharField(max_length=50, blank=True, null=True)
    applicant = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Premise Payment Table'


class PrincipleLicence(models.Model):
    licence_type = models.CharField(max_length=100, blank=True, null=True)
    purpose_of_application = models.CharField(max_length=100, blank=True, null=True)
    previous_licence_number = models.CharField(max_length=100, blank=True, null=True)
    certificate_number = models.CharField(max_length=200, blank=True, null=True)
    name_of_the_company = models.CharField(max_length=50, blank=True, null=True)
    company_status = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(max_length=30, blank=True, null=True)
    sub_county = models.CharField(max_length=30, blank=True, null=True)
    parish = models.CharField(max_length=30, blank=True, null=True)
    village = models.CharField(max_length=30, blank=True, null=True)
    application_fee = models.IntegerField(blank=True, null=True)
    licence_fee = models.IntegerField(blank=True, null=True)
    projected_gross_turnover = models.TextField(blank=True, null=True)
    previous_business_engagement = models.CharField(max_length=3, blank=True, null=True)
    name_of_the_business = models.CharField(max_length=30, blank=True, null=True)
    engagement_capacity = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    crime_engagement = models.CharField(max_length=30, blank=True, null=True)
    crime_details = models.CharField(max_length=30, blank=True, null=True)
    is_confirmed = models.BooleanField()
    email = models.CharField(max_length=50, blank=True, null=True)
    memorandum_and_articles_of_association = models.CharField(max_length=100, blank=True, null=True)
    districts_of_conduction = models.CharField(max_length=100, blank=True, null=True)
    annual_company_returns = models.CharField(max_length=100, blank=True, null=True)
    tenancy_agreement = models.CharField(max_length=100, blank=True, null=True)
    categories_of_machines = models.CharField(max_length=100, blank=True, null=True)
    class_of_the_casino_games = models.CharField(max_length=50, blank=True, null=True)
    purpose_of_the_lottery = models.CharField(max_length=50, blank=True, null=True)
    inspection_authority_status = models.CharField(max_length=30, blank=True, null=True)
    inspection_authority_remarks = models.TextField(blank=True, null=True)
    forward_for_verification = models.BooleanField()
    inspection_report = models.CharField(max_length=100, blank=True, null=True)
    defer_to_inspector = models.BooleanField()
    date_inspected = models.DateTimeField(blank=True, null=True)
    verification_authority_status = models.CharField(max_length=30, blank=True, null=True)
    verification_authority_remarks = models.TextField(blank=True, null=True)
    forward_for_approval = models.BooleanField()
    defer_to_verifier = models.BooleanField()
    date_verified = models.DateTimeField(blank=True, null=True)
    manager_remarks = models.TextField(blank=True, null=True)
    date_assigned = models.DateField(blank=True, null=True)
    assigned = models.BooleanField()
    approving_authority_status = models.CharField(max_length=30, blank=True, null=True)
    approving_authority_remarks = models.TextField(blank=True, null=True)
    approved = models.BooleanField()
    date_approved = models.DateField(blank=True, null=True)
    date_applied = models.DateField(blank=True, null=True)
    expiry_date = models.CharField(max_length=30, blank=True, null=True)
    applicant = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    applicationfeepayments = models.ForeignKey('PaymentsApplicationfeepayments', models.DO_NOTHING, blank=True, null=True)
    approved_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    assigned_to_inspector = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    bank_guarantee = models.ForeignKey(BankGuarantee, models.DO_NOTHING, blank=True, null=True)
    inspected_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    licencefeepayments = models.ForeignKey('PaymentsLicencefeepayments', models.DO_NOTHING, blank=True, null=True)
    verified_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    ura_county = models.CharField(max_length=50, blank=True, null=True)
    ura_district = models.CharField(max_length=50, blank=True, null=True)
    ura_subcounty = models.CharField(max_length=50, blank=True, null=True)
    ura_village = models.CharField(max_length=50, blank=True, null=True)
    tin = models.IntegerField(blank=True, null=True)
    plot_number = models.CharField(max_length=50, blank=True, null=True)
    validity = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Principle Licence'


class PrincipleLicenceRenewal(models.Model):
    previous_licence_number = models.CharField(max_length=5)
    previous_licence_number_type = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=30, blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(db_column='County', max_length=30, blank=True, null=True)  # Field name made lowercase.
    subcounty = models.CharField(db_column='SubCounty', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parish = models.CharField(db_column='Parish', max_length=30, blank=True, null=True)  # Field name made lowercase.
    village = models.CharField(db_column='Village', max_length=30, blank=True, null=True)  # Field name made lowercase.
    licence_fee = models.IntegerField(blank=True, null=True)
    projected_gross_turnover = models.IntegerField(db_column='Projected_Gross_Turnover', blank=True, null=True)  # Field name made lowercase.
    previous_engagement = models.CharField(db_column='Previous_Engagement', max_length=3, blank=True, null=True)  # Field name made lowercase.
    name_of_the_business = models.CharField(db_column='Name_of_the_business', max_length=30, blank=True, null=True)  # Field name made lowercase.
    capacity = models.CharField(db_column='Capacity', max_length=30, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    crime_history = models.CharField(db_column='Crime_History', max_length=30, blank=True, null=True)  # Field name made lowercase.
    crime_details = models.CharField(db_column='Crime_Details', max_length=30, blank=True, null=True)  # Field name made lowercase.
    is_confirmed = models.BooleanField()
    date_applied = models.DateField(blank=True, null=True)
    districts_of_conduction = models.CharField(max_length=200, blank=True, null=True)
    annual_company_returns = models.CharField(max_length=200, blank=True, null=True)
    tenacy_agreement = models.CharField(max_length=200, blank=True, null=True)
    inspection_authority_status = models.CharField(max_length=30, blank=True, null=True)
    inspection_authority_remarks = models.TextField(blank=True, null=True)
    inspected = models.BooleanField()
    date_inspected = models.DateTimeField(blank=True, null=True)
    verification_authority_status = models.CharField(max_length=30, blank=True, null=True)
    verification_authority_remarks = models.TextField(blank=True, null=True)
    verified = models.BooleanField()
    date_verified = models.DateTimeField(blank=True, null=True)
    approving_authority_status = models.CharField(max_length=30, blank=True, null=True)
    approved = models.BooleanField()
    date_approved = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    applicant = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    approved_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    bank_guarantee = models.ForeignKey('RenewalBankGuarantee', models.DO_NOTHING, blank=True, null=True)
    inspected_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)
    verified_by = models.ForeignKey('AccountAccount', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Principle Licence Renewal'


class RenewalBankGuarantee(models.Model):
    date_created = models.DateField()
    rinciple_licence_certificate_number = models.CharField(max_length=50)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=30, blank=True, null=True)
    bank = models.CharField(max_length=70, blank=True, null=True)
    bank_guarantee = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Renewal Bank Guarantee '


class AccountAccount(models.Model):
    password = models.CharField(max_length=128)
    email = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    card_number = models.CharField(max_length=9, blank=True, null=True)
    district = models.CharField(db_column='District', max_length=30, blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(db_column='County', max_length=30, blank=True, null=True)  # Field name made lowercase.
    subcounty = models.CharField(db_column='Subcounty', max_length=30, blank=True, null=True)  # Field name made lowercase.
    parish = models.CharField(db_column='Parish', max_length=30, blank=True, null=True)  # Field name made lowercase.
    village = models.CharField(db_column='Village', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone_number = models.CharField(unique=True, max_length=100)
    sex = models.CharField(max_length=200)
    image = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField()
    is_admin = models.BooleanField()
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    role = models.CharField(max_length=200)
    legalstatus = models.CharField(db_column='legalStatus', max_length=200, blank=True, null=True)  # Field name made lowercase.
    citizenship = models.CharField(max_length=200, blank=True, null=True)
    nin = models.CharField(max_length=14, blank=True, null=True)
    ppn = models.CharField(max_length=14, blank=True, null=True)
    wpn = models.CharField(max_length=14, blank=True, null=True)
    business_registration_date = models.CharField(max_length=200, blank=True, null=True)
    brn = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_account'


class AccountAccountGroups(models.Model):
    account = models.ForeignKey(AccountAccount, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_account_groups'
        unique_together = (('account', 'group'),)


class AccountAccountUserPermissions(models.Model):
    account = models.ForeignKey(AccountAccount, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_account_user_permissions'
        unique_together = (('account', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountAccount, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Oauth2ProviderAccesstoken(models.Model):
    token = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.ForeignKey('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountAccount, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    source_refresh_token = models.OneToOneField('Oauth2ProviderRefreshtoken', models.DO_NOTHING, blank=True, null=True)
    id_token = models.OneToOneField('Oauth2ProviderIdtoken', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(AccountAccount, models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    algorithm = models.CharField(max_length=5)
    client_secret = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.TextField()
    scope = models.TextField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(AccountAccount, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    code_challenge = models.CharField(max_length=128)
    code_challenge_method = models.CharField(max_length=10)
    nonce = models.CharField(max_length=255)
    claims = models.TextField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderIdtoken(models.Model):
    jti = models.CharField(unique=True, max_length=32)
    expires = models.DateTimeField()
    scope = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_idtoken'


class Oauth2ProviderRefreshtoken(models.Model):
    token = models.CharField(max_length=255)
    access_token = models.OneToOneField(Oauth2ProviderAccesstoken, models.DO_NOTHING, blank=True, null=True)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(AccountAccount, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    revoked = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'
        unique_together = (('token', 'revoked'),)


class PaymentsApplicationfeepayments(models.Model):
    application_fee = models.IntegerField(blank=True, null=True)
    generate_prn = models.BooleanField()
    tin = models.IntegerField(blank=True, null=True)
    prn = models.IntegerField(blank=True, null=True)
    error_code = models.CharField(max_length=30, blank=True, null=True)
    error_desc = models.CharField(max_length=30, blank=True, null=True)
    search_code = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    payment_expiry_date = models.CharField(max_length=30, blank=True, null=True)
    payment_registered_on = models.CharField(max_length=30, blank=True, null=True)
    payment_made_by = models.CharField(max_length=30, blank=True, null=True)
    payment_made_on = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments_applicationfeepayments'


class PaymentsLicencefeepayments(models.Model):
    licence_fee = models.IntegerField(blank=True, null=True)
    generate_prn_licence_fee = models.BooleanField()
    licence_fee_tin = models.IntegerField(blank=True, null=True)
    licence_fee_prn = models.IntegerField(blank=True, null=True)
    licence_fee_error_code = models.CharField(max_length=30, blank=True, null=True)
    licence_fee_error_desc = models.CharField(max_length=30, blank=True, null=True)
    licence_fee_search_code = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(max_length=30, blank=True, null=True)
    payment_description = models.CharField(max_length=30, blank=True, null=True)
    payment_expiry_date = models.CharField(max_length=30, blank=True, null=True)
    payment_registered_on = models.CharField(max_length=30, blank=True, null=True)
    payment_made_by = models.CharField(max_length=30, blank=True, null=True)
    payment_made_on = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments_licencefeepayments'


class RenewPremiselicencerenewalmodel(models.Model):
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'renew_premiselicencerenewalmodel'
