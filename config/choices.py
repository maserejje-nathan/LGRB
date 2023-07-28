from datetime import datetime

licence =[
    (None, 'Choose an action'),
    ('License to conduct a National Lottery','License to conduct a National Lottery'),
    ('License to conduct a Public Lottery','License to conduct a Public Lottery'),
    ('Casino operating license','Casino operating license'),
    ('Bingo betting license','Bingo betting license'),
    ('Pool betting license','Pool betting license'),
    ('Betting Intermediary operating license','Betting Intermediary operating license'), 
    
    ('Gaming or betting machine general operating license','Gaming or betting machine general operating license'),
    ('Gaming or betting machine techinical operating license','Gaming or betting machine techinical operating license'),
    
    ('General betting operating license','General betting operating license'),
    ('Gambling software operating license','Gambling software operating license'),
]

year_choices = [
    (year, year) for year in range(datetime.now().year, datetime.now().year - 10, -1)
]

purpose =[
    (None, 'Choose an action'),
    ('New','New'),
    ('Renewal','Renewal'),
]

BOOL_CHOICE = [
    (None, 'Choose an action'),
    ('Yes','Yes'),
    ('No', 'No')
]

PRICECATEGORY = {
    (None, 'Choose an action'),
    ('Licence Fee','Licence Fee'),
    ('Application Fee', 'Application Fee')
}
COMPANY_STATUS = (
    (None, 'Choose an action'),
    ('Foreign','Foreign'),
    ('National', 'National')
)

SUITABLE_CHOICE = (
    (None, 'Choose suitability'),
    ('Suitable','Suitable'),
    ('Not suitable', 'Not suitable'),
    ('Does not apply ', 'Does mot apply')
)

YESNO_CHOICE = (
    (None, 'Choose an action'),
    ('Yes','Yes'),
    ('No', 'No')
)

AVAILABLE_CHOICE = (
    (None, 'Choose availability'),
    ('Available','Available'),
    ('Not available', 'Not available'),
)

DISPLAY_CHOICE = (
     (None, 'Choose display status'),
    ('Displayed','Displayed'),
    ('Not displayed', 'Not displayed'),
)
PRICE_CHOICE = {
    (None, 'Choose an action'),
    ('Foreigner','Foreigner'),
    ('National', 'National')
}

roles = [
    (None, 'Choose an action'),
    ('inspector','inspector'),
    ('verifier', 'verifier'),
    ('approver', 'approver'),
    ('admin', 'admin'),
    ('client', 'client')
]

roles_trimed = [
    (None, 'Choose an action'),
    ('inspector','inspector'),
    ('verifier', 'verifier'),
    ('approver', 'approver'),
    ('admin', 'admin'),
]

PURPOSE_CHOICE = [
    (None, 'Choose an action'),
    ('New application','New application'),
    ('Renewal', 'Renewal')
]

legalStatus = [
    (None, 'Type of Applicant'),
    ('Individual','Individual'),
    ('Company', 'Company'),
]

citizenship = [
    (None, 'Choose Citizenship'),
    ('Ugandan','Ugandan'),
    ('Non-Ugandan', 'Non-Ugandan'),
]

sex = [
    (None, 'Choose Gender'),
    ('Male','Male'),
    ('Female', 'Female'),
]

validity = [
     ('Valid','Valid'),
    ('Expired', 'expired'),
]

LICENCE_TYPE = [
    (None, 'Choose Type'),
    ('Principle Licence','Principle Licence'),
    ('Employee Licence', 'Employee Licence'),
    ('Premise Licence', 'Premise Licence'),
]


CITITZENSHIP_TYPE = [
    (None, 'Choose Type'),
    ('Ugandan','Ugandan'),
    ('Non-Ugandan', 'Non-Ugandan')
]


# inspection_choices = [
#     (None, 'Choose an action'),
#     ('Recomended for a licence','Recomended for a licence'),
#     ('Does not meet creteria', 'Does not meet creteria'),
# ]
# verification_choices = [
#     (None, 'Choose an action'),
#     ('Recomended for approval','Recomended for approval'),
#     ('Recomended for rejection', 'Recomended for rejection'),
#     ('Defered', 'Defered'),
# ]
# approved_choices = [
#     (None, 'Choose an action'),
#     ('Approved','Approved'),
#     ('Rejected', 'Rejected'),
#     ('Defered', 'Defered'),
# ]


inspection_choices = [
    (None, 'Choose an action'),
    ('Recomended for a licence','Recomended for a licence'),
    ('Recomended for rejection', 'Recomended for rejection'),
]

verification_choices = [
    (None, 'Choose an action'),
    ('Recomended for approval','Recomended for approval'),
    ('Recomended for rejection', 'Recomended for rejection'),
    ('Defered', 'Defered'),
]

approved_choices = [
    (None, 'Choose an action'),
    ('Approved','Approved'),
    ('Rejected', 'Rejected'),
    ('Defered', 'Defered'),
]


bank_guarantee_verification_choices = [
    (None, 'Choose an action'),
    ('Recomended for approval','Recomended for approval'),
    ('Recomended for rejection', 'Recomended for rejection'),
]

bank_guarantee_approved_choices = [
    (None, 'Choose an action'),
    ('Approved','Approved'),
    ('Rejected', 'Rejected')
]

occupation = [
    (None , 'Choose an action'),
    ('CEO', 'CEO'),
    ('Premise Manager', 'Premise Manager'),
    ('Finance Manager','Finance Manager'),
    ('IT Manager', 'IT Manager'),
    ('Cashier', 'Cashier'),
    ('PIT Boss', 'PIT Boss'),
    ('Dealer', 'Dealer')
]


REGION_CHOICES = [
    (None , 'Choose an region'),
    ('Western', 'Western'),
    ('Eastern ','Eastern '),
    ('Northern', 'Northern'),
    ('West Nile', 'West Nile'),
    ('Buganda ', 'Buganda '),
    ('KMP', 'KMP'),
]



districts = [
    (None, 'Choose an action'),
    ('ABIM', 'ABIM'),
    ('ADJUMANI', 'ADJUMANI'),
    ('AGAGO', 'AGAGO'),
    ('ALEBTONG', 'ALEBTONG'),
    ('AMOLATAR', 'AMOLATAR'),
    ('AMUDAT', 'AMUDAT'),
    ('AMURIA', 'AMURIA'),
    ('AMURU', 'AMURU'),
    ('APAC', 'APAC'),
    ('ARUA', 'ARUA'),
    ('BUDAKA', 'BUDAKA'),
    ('BUDUDA', 'BUDUDA'),
    ('BUGIRI', 'BUGIRI'),
    ('BUGWERI', 'BUGWERI'),
    ('BUHWEJU', 'BUHWEJU'),
    ('BUIKWE', 'BUIKWE'),
    ('BUKEDEA', 'BUKEDEA'),
    ('BUKOMANSIMBI', 'BUKOMANSIMBI'),
    ('BUKWO', 'BUKWO'),
    ('BULAMBULI', 'BULAMBULI'),
    ('BULIISA', 'BULIISA'),
    ('BUNDIBUGYO', 'BUNDIBUGYO'),
    ('BUNYANGABU', 'BUNYANGABU'),
    ('BUSHENYI', 'BUSHENYI'),
    ('BUSIA', 'BUSIA'),
    ('BUTALEJA', 'BUTALEJA'),
    ('BUTAMBALA', 'BUTAMBALA'),
    ('BUTEBO', 'BUTEBO'),
    ('BUVUMA', 'BUVUMA'),
    ('BUYENDE', 'BUYENDE'),
    ('DOKOLO', 'DOKOLO'),
    ('GOMBA', 'GOMBA'),
    ('GULU', 'GULU'),
    ('HOIMA', 'HOIMA'),
    ('IBANDA', 'IBANDA'),
    ('IGANGA', 'IGANGA'),
    ('ISINGIRO', 'ISINGIRO'),
    ('JINJA', 'JINJA'),
    ('KAABONG', 'KAABONG'),
    ('KABALE', 'KABALE'),
    ('KABAROLE', 'KABAROLE'),
    ('KABERAMAIDO', 'KABERAMAIDO'),
    ('KAGADI', 'KAGADI'),
    ('KAKUMIRO', 'KAKUMIRO'),
    ('KALAKI', 'KALAKI'),
    ('KALANGALA', 'KALANGALA'),
    ('KALIRO', 'KALIRO'),
    ('KALUNGU', 'KALUNGU'),
    ('KAMPALA', 'KAMPALA'),
    ('KAMULI', 'KAMULI'),
    ('KAMWENGE', 'KAMWENGE'),
    ('KANUNGU', 'KANUNGU'),
    ('KAPCHORWA', 'KAPCHORWA'),
    ('KAPELEBYONG', 'KAPELEBYONG'),
    ('KARENGA', 'KARENGA'),
    ('KASANDA', 'KASANDA'),
    ('KASESE', 'KASESE'),
    ('KATAKWI', 'KATAKWI'),
    ('KAYUNGA', 'KAYUNGA'),
    ('KAZO', 'KAZO'),
    ('KIBAALE', 'KIBAALE'),
    ('KIBOGA', 'KIBOGA'),
    ('KIBUKU', 'KIBUKU'),
    ('KIKUUBE', 'KIKUUBE'),
    ('KIRUHURA', 'KIRUHURA'),
    ('KIRYANDONGO', 'KIRYANDONGO'),
    ('KISORO', 'KISORO'),
    ('KITAGWENDA', 'KITAGWENDA'),
    ('KITGUM', 'KITGUM'),
    ('KOBOKO', 'KOBOKO'),
    ('KOLE', 'KOLE'),
    ('KOTIDO', 'KOTIDO'),
    ('KUMI', 'KUMI'),
    ('KWANIA', 'KWANIA'),
    ('KWEEN', 'KWEEN'),
    ('KYANKWANZI', 'KYANKWANZI'),
    ('KYEGEGWA', 'KYEGEGWA'),
    ('KYENJOJO', 'KYENJOJO'),
    ('KYOTERA', 'KYOTERA'),
    ('LAMWO', 'LAMWO'),
    ('LIRA', 'LIRA'),
    ('LUUKA', 'LUUKA'),
    ('LUWEERO', 'LUWEERO'),
    ('LWENGO', 'LWENGO'),
    ('LYANTONDE', 'LYANTONDE'),
    ('MADI-OKOLLO', 'MADI-OKOLLO'),
    ('MANAFWA', 'MANAFWA'),
    ('MARACHA', 'MARACHA'),
    ('MASAKA', 'MASAKA'),
    ('MASINDI', 'MASINDI'),
    ('MAYUGE', 'MAYUGE'),
    ('MBALE', 'MBALE'),
    ('MBARARA', 'MBARARA'),
    ('MITOOMA', 'MITOOMA'),
    ('MITYANA', 'MITYANA'),
    ('MOROTO', 'MOROTO'),
    ('MOYO', 'MOYO'),
    ('MPIGI', 'MPIGI'),
    ('MUBENDE', 'MUBENDE'),
    ('MUKONO', 'MUKONO'),
    ('NABILATUK', 'NABILATUK'),
    ('NAKAPIRIPIRIT', 'NAKAPIRIPIRIT'),
    ('NAKASEKE', 'NAKASEKE'),
    ('NAKASONGOLA', 'NAKASONGOLA'),
    ('NAMAYINGO', 'NAMAYINGO'),
    ('NAMISINDWA', 'NAMISINDWA'),
    ('NAMUTUMBA', 'NAMUTUMBA'),
    ('NAPAK', 'NAPAK'),
    ('NEBBI', 'NEBBI'),
    ('NGORA', 'NGORA'),
    ('NTOROKO', 'NTOROKO'),
    ('NTUNGAMO', 'NTUNGAMO'),
    ('NWOYA', 'NWOYA'),
    ('OBONGI', 'OBONGI'),
    ('OMORO', 'OMORO'),
    ('OTUKE', 'OTUKE'),
    ('OYAM', 'OYAM'),
    ('PADER', 'PADER'),
    ('PAKWACH', 'PAKWACH'),
    ('PALLISA', 'PALLISA'),
    ('RAKAI', 'RAKAI'),
    ('RUBANDA', 'RUBANDA'),
    ('RUBIRIZI', 'RUBIRIZI'),
    ('RUKIGA', 'RUKIGA'),
    ('RUKUNGIRI', 'RUKUNGIRI'),
    ('RWAMPARA', 'RWAMPARA'),
    ('SERERE', 'SERERE'),
    ('SHEEMA', 'SHEEMA'),
    ('SIRONKO', 'SIRONKO'),
    ('SOROTI', 'SOROTI'),
    ('SSEMBABULE', 'SSEMBABULE'),
    ('TORORO', 'TORORO'),
    ('WAKISO', 'WAKISO'),
    ('YUMBE', 'YUMBE'),
    ('ZOMBO', 'ZOMBO'),
    ]
    