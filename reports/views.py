from django.shortcuts import render
from django.http import HttpResponse
from account.models import Account 
from administrator.models import *
from new.models import *
from reports.forms import * 

from django.db.models import Sum, Count
from django.db.models import Aggregate
from django.db.models.functions import Coalesce
from django.db.models import F, FloatField, ExpressionWrapper

from io import BytesIO, StringIO
from django.views import View
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
 
import csv
import json 
from json import JSONEncoder as jencoder
from datetime import date


class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString( 205 * mm, 10 * mm + (0.2 * inch), "Page %d of %d" % (self._pageNumber, page_count))


class PrintUsersPDF(View):

    def get(self, request, *args, **kwargs):

        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 
            rightMargin=50,
            leftMargin=50,
            topMargin=72,
            bottomMargin=60,
            pagesize=A4
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30



        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = Account.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        for  user in users:
            elements.append(
                Paragraph((user.email), styles['Normal'])
            )


        elements.append(
            Paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent commodo erat dolor, in vulputate leo accumsan ac. Vivamus pulvinar lacus sit amet nisl dictum, nec malesuada mauris porta. Phasellus varius mi non dui pretium interdum convallis vel nisl. Duis egestas scelerisque fermentum. Aliquam finibus metus sollicitudin, fringilla nunc vel, facilisis elit. Cras ut accumsan ligula, a interdum augue. In eu elementum arcu, eget laoreet felis. Morbi vulputate aliquam augue, quis scelerisque diam pulvinar eu. Sed malesuada dignissim laoreet. Morbi convallis dolor at pulvinar luctus. Sed interdum quam eu nunc tincidunt henPhasellus placerat neque id neque consectetur consectetur. Curabitur nisl justo, consequat ac ornare ac, congue varius magna. Sed enim nisi, posuere vitae nibh vitae, accumsan luctus nisl. Vivamus quis purus eu dui vulputate accumsan. In hac habitasse platea dictumst. Maecenas vitae sodales erat. Duis semper vestibulum justo, a ultricies ante malesuada conseDonec semper euismod mauris ut lacinia. Donec sollicitudin, ipsum id finibus placerat, est libero fringilla metus, sed sollicitudin lectus est at felis. Nunc nec turpis non nisi pharetra congue. Suspendisse cursus turpis ac mattis luctus. Vivamus quam nunc, efficitur eu faucibus et, condimentum vitae lacus. Phasellus luctus quam ipsum, et blandit nibh finibus sit amet. Cras fermentum sollicitudin egestas. Maecenas erat ante, fringilla eu augue vitae, viverra vehicula neque. Vivamus auctor erat vel vestibulum lobortis. Aliquam et sapien porttitor, egestas libero quis, vehicula dolor. Nunc eu massa pharetra, viverra purus non, pulvinar erat. Nam in nibhNulla porttitor dapibus odio. Etiam vitae ornare velit, non imperdiet quam. Vestibulum lacinia vel justo a lobortis. Proin vehicula nisi vitae ex tincidunt blandit. Donec a magna vel odio fermentum elementum. Duis eget odio mauris. Sed pretium suscipit lacus, vitae vehicula mauris. Vivamus arcu sapien, elementum non est a, rhoncus elementum nisl. Integer ut justo lacus. Phasellus convallis tempus facilisis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Praesent in justo vitae odio accumsan pharetra in utauris venenatis eget sapien in dictum. Aliquam et bibendum lectus. Suspendisse potenti. Sed urna ipsum, aliquet eget sollicitudin eu, molestie ut nisi. Fusce ligula neque, posuere quis tincidunt vel, dignissim sit amet dolor. Sed vel ipsum ligula. In quis odio vel leo eleifend varius vel sit amet lorem. Mauris malesuada euismod elementum. Curabitur laoreet est vitae enim cursus, et porta neque hendrerit. Aliquam nunc ipsum, pulvinar quis finibus sit amet, fermentum eget ex. Sed eu ligula eu arcu lobortis suscipit. Pellentesque ultricies odio nec dui cursus ultricies. Fusce vitae suscipit ipsum. Ut metus nisl, dapibus ac velit sed, dapibus luctus tellus. Proin at quam egestas, maximus eros quis, semper as at aliquam neque. Duis tempus massa felis, vel viverra leo tristique ac. Nam suscipit lobortis magna et euismod. Vivamus sollicitudin justo mauris, sit amet efficitur augue feugiat eget. Phasellus placerat, magna sit amet eleifend euismod, nisl nunc blandit eros, eget bibendum velit purus quis lacus. Integer ultrices purus non turpis rhoncus, ut mollis est semper. Donec sapien nibh, fermentum ut erat vitae, tempus gravida eros. Nam pellentesque vestibulum euismod. Integer in turpis ultrices, suscipit eros id, ornare ante. Pellentesque dignissim maximus interdum. Aenean vestibulum risus ut augue laoreet, vel feugiat est aliquet. Morbi vel velit sit amet massa molestie aliquam. Aliquam erat volutpat. Morbi eget pretium diam, id bibendum usce maximus massa at risus molestie sagittis. Curabitur in aliquam lorem. Praesent tincidunt sagittis luctus. Proin egestas ullamcorper velit, nec interdum lacus rutrum id. Pellentesque viverra aliquet diam id aliquam. Praesent vehicula odio at augue convallis, et congue libero cursus. Duis ut mi at risus rhoncus commodo. Nulla ultricies sem sit amet magna rutrum, pretium porta augue venenatis. Nunc blandit libero non mauris tempus luctus. Morbi vulputate lobortis euismod. Curabitur sodales imperdiet faucibus. Quisque semper sem nulla, vel dignissim metus ullamcorper vulpullentesque tortor leo, feugiat vitae cursus vestibulum, iaculis ut lacus. Vestibulum mattis, lacus interdum luctus ullamcorper, diam ligula tempus enim, et facilisis nisi magna ut orci. Nam enim massa, ultrices id ultricies in, tempor tincidunt orci. Integer aliquet arcu interdum, euismod orci in, mollis sem. Aliquam vel orci commodo, vulputate nisl eu, elementum libero. Sed est nulla, aliquet sed fringilla sed, condimentum sed massa. Etiam eu aliquam diam, ut fermentum nibh. Aliquam euismod odio a accumsan aliquet. Mauris maximus tempor consequat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nam dignissim aliquet euismod. Phasellus ac nisl posuere, porta turpis quis, euismod dui. Fusce in gravida leo, sed blandit aesent lacinia ante quis euismod luctus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut sagittis pretium malesuada. Curabitur blandit fringilla sem, vitae varius dui porttitor sit amet. Sed auctor est et maximus feugiat. Vestibulum arcu justo, imperdiet ac dignissim et, dictum vitae est. Fusce at ipsum aliquet, dictum enim ut, eleifend lectus. Donec maximus, diam non vulputate porta, arcu mauris rutrum diam, vitae tempus sapien eros sit amet turpis. Donec quis magna sollicitudin, venenatis ante non, elementum dui. Cras eu turpis nec ut mattis nulla, ac sagittis dolor. In eleifend ultricies elit, vel tristique metus pulvinar ut. Suspendisse in risus massa. Proin sodales mauris eu lorem ultricies, mattis tempor risus convallis. Duis congue dolor dolor, semper sagittis metus semper at. Nulla eget fermentum nulla, non pellentesque dolor. Fusce rutrum iaculis urna, at venenatis erat porttitor sed. Donec ut leo elit. In id leo dolor. Maecenas sagittis, mi sit amet venenatis lobortis, sem nisl maximus risus, et consectetur ante sem sed felis. Etiam quis ipsum pretium, blandit libero sed, mattis am eget imperdiet nisi. Fusce malesuada efficitur lectus, non dictum purus. Suspendisse iaculis egestas tristique. Maecenas ornare euismod orci, ac aliquet dolor finibus sed. Nunc vitae diam odio. Ut lobortis ipsum nec justo convallis vehicula. Suspendisse luctus justo metus, et cursus tortor conguvamus vitae lorem sed enim pulvinar cursus. Phasellus imperdiet eleifend arcu eu ornare. Fusce varius, est a lobortis accumsan, ex augue blandit ex, id pellentesque tortor enim non urna. Mauris volutpat nulla ac risus aliquet elementum. Suspendisse lobortis aliquet lacus. In sit amet ornare dolor. Duis vulputate faucibus risus, eu dapibus sapien aliquam sit amet. In eget turpis maximus, congue mi a, fringilla erc pulvinar risus neque, eu vestibulum neque efficitur eu. Donec venenatis eros sed mauris vestibulum, nec condimentum ante fringilla. Vestibulum sodales eleifend nunc at fringilla. Praesent fringilla tellus et sollicitudin sodales. Sed congue elit ipsum, non egestas erat dignissim quis. Maecenas sodales vehicula tempus. Etiam ut mattis dui, vitae mollis quam. Sed sit amet bibendum metus, in faucibus sapien. Etiam sed viverra elit, eu condimentum mauris. Vestibulum aliquet purus ac mauris eleifend maximus. Donec libero mauris, scelerisque sit amet elit vel, vehicula fermentum sapien. In faucibus neque nulla, vel iaculis massa imperdiet ac. Vivamus laoreet neque sed ultrices digniscenas id venenatis magna. Mauris tincidunt libero vel ligula sodales cursus sed sed risus. Quisque ut maximus purus. Maecenas dictum vitae nisi non condimentum. Donec eu sapien arcu. Donec et lobortis eros. Ut imperdiet orci nec mi efficitur tempus. Aenean eget tristique libris faucibus nisi at eros laoreet pulvinar. Proin laoreet leo vitae turpis iaculis dignissim. Quisque gravida nisl dui, sit amet tincidunt lectus rutrum vel. Nunc lobortis nulla eget enim venenatis, id convallis turpis porta. Nullam vestibulum cursus feugiat. Praesent condimentum consequat augue ut mattis. Duis sollicitudin ipsum ligula, at commodo nunc dictum id. Aenean rhoncus felis sit amet faucibus laoreet. Sed convallis accumsan neque egestas fringilla. Ut eu ullamcorper tellus. Sed purus nunc, blandit id iaculis sed, sollicitudin ut arcu. Etiam tempor purus mi, ac porttitor metus congue q ornare ante tellus, vitae interdum nisl pellentesque in. Vivamus porttitor vel est at euismod. Ut vel imperdiet dolor. Donec sagittis accumsan sodales. Duis sit amet ipsum pharetra lectus dictum commodo. Aenean pharetra neque nulla. Donec in ipsum lacus. Donec nec rutrum enim. Aenean ac metus augue. Etiam rutrum lectus ut odio sodales, id aliquam orci posuere. Ut vitae nulla orci. Praesent molestie sem a neque ultrices finibus. Mauris efficitur aliquet ullamcorper. Sed euismod, nisi vel imperdiet fringilla, ex dui varius nunc, ut dictum mauris magna non neque. Donec sollicitudin mollis quam, vitae lobortis rbi nec vehicula risus. Sed sodales neque nec felis efficitur varius. Duis eget ipsum pellentesque, ullamcorper libero non, fermentum lectus. Nunc luctus risus fermentum, congue tortor ut, sodales sapien. Mauris rutrum mauris diam, in suscipit nisl pretium vel. Integer sodales vitae augue id pulvinar. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Integer auctor tortor elit, id interdum mi blandit at. Curabitur aliquam turpis ac mauris posuere ultrices. Nam quis orci tempor, porttitor odio id, vestibulum dui. Nulla facilisi. Vestibulum quis molestie velit. Ut molestie cursus lacus sed dictum. Quisque vel suscipit ligula. Donec vitae congue ecenas id lacus nec est luctus porttitor. Nullam augue sapien, dictum ut laoreet nec, aliquet eget lorem. Praesent felis mauris, fermentum sed sollicitudin vel, malesuada ac quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse a suscipit justo. Pellentesque blandit dui ut sem pharetra scelerisque. In efficitur, risus vel varius viverra, ex mi sodales libero, et sollicitudin turpis turpis a diam. Donec a enim lorem. Nulla leo quam, congue non rutrum ut, cursus a lectus. Phasellus libero diam, sollicitudin eget enim eu, elementum bibendum sem. Aliquam nec dolor mi. Duis pretium tincidunt ligula, finibus semper erat gravida in. Pellentesque in ligula ut ante egestas pulvinar nec et nquam eu metus risus. Quisque eget lectus dolor. In a lobortis risus. Ut molestie dui at erat venenatis semper. Quisque sed sapien eget nulla vehicula rutrum. Aliquam pharetra blandit lorem eget vestibulum. Morbi ut ipsum sollicitudin, porttitor nibh eu, vestibulum est. Vivamus vel quam feugiat, tempus dui sed, aliquet orci. Nam iaculis lectus erat, ut hendrerit purus sodales quis. Vivamus finibus egestas sagittis. Sed lobortis eu dui sit amet volutpat. Vivamus maximus porta urna, nec vestibulum urna blandit et. Donec consequat justo ac risus egestas convallis. Donec sodales auctor ligula. Pellentesque scelerisque, quam tincidunt tempus mollis, felis erat laoreet purus, quis finibus lectus nulla eget sapien. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egesec in scelerisque justo. Pellentesque ac congue augue, et fringilla urna. Donec scelerisque eros id rutrum mattis. Quisque molestie eget elit quis molestie. Sed finibus justo eu lorem varius dapibus. Nunc vitae molestie nisl. Aenean rhoncus ut mi in porttitor. Pellentesque eget nisl luctus, ultrices magna et, eleifend nisl. Maecenas convallis iaculis euismod. Vivamus sollicitudin ligula felis, ac pharetra nisi eleifend sed. Maecenas imperdiet eu nibh vel aliquam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eros mauris, tempus sollicitudin consectetur id, bibendum a eros. Donec in sem et tellus malesuada consectetur et interdum doc commodo consectetur rutrum. Phasellus interdum ornare tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus faucibus sit amet nunc ac varius. Phasellus scelerisque tincidunt nisl nec mattis. Vivamus tempus, nunc sed bibendum ultricies, diam neque luctus enim, non gravida massa risus lobortis purus. Nulla finibus neque vitae ante ultricies, in tincidunt quam condimentum. Nam molestie porta ornare. Mauris vitae enim a dolor maximus mattis. Duis in eros viverra, pulvinar turpis placerat, lacinia mi. Praesent vehicula velit non leo pulvinar vehicula. Nam eu tristique tortor, tristique dictum magna. Donec id enim in est ornare tristique. Sed sagittis ac felis quis venenasapien nibh, imperdiet eu orci nec, condimentum venenatis dolor. Proin a odio quis ex volutpat fermentum. Sed vestibulum vel erat quis tincidunt. Sed eleifend justo lobortis viverra ultricies. Donec est tortor, porta ac lorem eget, tristique imperdiet urna. Donec in nibh sit amet arcu pharetra suscipit. Etiam bibendum, lorem et sagittis feugiat, velit eros ornare elit, non lobortis justo nisi non quam. Cras auctor varius dignam mattis id lacus in volutpat. Sed nec arcu nisl. Fusce sem ligula, facilisis sed neque sed, interdum pulvinar quam. Vestibulum urna est, laoreet vitae condimentum ut, pulvinar quis dolor. Integer ac magna at sapien dictum posuere eu nec felis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vehicula tristique urna, non congue lectus placerat sed. Nunc non tristique nibh. Sed ornare mollis nisl vitae faucibus. Ut porta elementum libero ac lacinia. Vestibulum ornare nisl id ante blandit accumsan. Aenean semper mollis ullamcorabitur ut orci eget mi sagittis molestie. Pellentesque viverra porta sem ut cursus. Curabitur interdum risus a est pellentesque tempus. Etiam viverra nibh in sem aliquet, bibendum varius quam luctus. Duis mollis nisl augue, non efficitur ipsum faucibus et. Nam in accumsan purus, nec congue dolor. Donec viverra elementum tellus ac tincidunt. In rhoncus risus at nunc viverra, nec egestas quam sodales. Maecenas facilisis vehicula nibh, quis molestie enim faucibus in. Sed ac lacus laoreet, dictum massa nec, dictum nibh. Nullam dictum diam id quam ultrices iacteger sit amet augue luctus, rutrum risus non, euismod tortor. Quisque blandit libero quis consequat commodo. Ut leo erat, consequat ut sollicitudin sit amet, gravida id nulla. Phasellus maximus sollicitudin mi non sagittis. Aenean auctor ut eros facilisis sollicitudin. Maecenas ullamcorper velit tellus, et dictum ligula cursus in. Aliquam pulvinar enim elit, fringilla vestibulum nisi sagittis at. Proin vitae lorem sollicitudin, scelerisque dolor nec, facilisis tortor. Cras tincidunt, sem at ullamcorper tincidunt, justo ligula vestibulum lorem, vitae hendrerit tellus risus quis justo. Sed eleifend ante tristique mi tincidunt condimentum et bibendum id efficitur pretium nisl, non venenatis nulla vehicula in. Duis vehicula finibus lectus nec rhoncus. Vivamus non auctor dui. Nam erat velit, faucibus vel odio ac, consequat interdum sapien. Proin euismod non elit eget euismod. Ut dictum sit amet libero vel accumsan. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras eu nunc libero. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Proin dapibus elit sed urna commodo rutrum. Fusce mauris urna, tempor id neque tincidunt, commodo scelerisque diam. Vestibulum pharetra hendrerit malesass aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi in efficitur tellus. Sed dictum feugiat gravida. Ut pharetra velit scelerisque ex tincidunt, nec dignissim lectus egestas. Proin ultricies nisl in turpis tincidunt, ac interdum dolor porta. Etiam sit amet est dignissim, faucibus diam congue, dignissim metus. Quisque a ex vitae nisl blandit consectetur. Curabitur vehicula molestie ante at blandit. Pellentesque eleifend malesuada gravida. Phasellus quis diam sed nibh dapibus iaculis sit amet luctus mroin eleifend erat ut malesuada finibus. Pellentesque in leo dapibus, condimentum justo vitae, vehicula metus. Duis aliquet, felis a porta malesuada, lacus arcu lobortis quam, vitae scelerisque quam eros id sem. Maecenas varius massa vitae justo cursus, id convallis urna mattis. Vivamus id congue ante, sed convallis felis. Suspendisse bibendum nisl quis neque dapibus aliquam. Fusce ac quam imperdiet, pellentesque ipsum et, dictum dui. Mauris nec efficitur elit. Nunc nisi tellus, fermentum et cursus eu, feugiat a quam. Sed dictum ligula sed tellus tempus laoreet. Sed at quam arcu. In gravida justo elit, nec rhoncus ligula vehicula vel. Quisque et mauris non felis venenatis malesuada ac et urna. Curabitur finibus diam ut augue posuere vehicula. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur quis ornare maecenas eget mi eleifend, auctor leo eget, convallis odio. Maecenas facilisis tortor a metus rhoncus suscipit. Nam sit amet neque pulvinar, facilisis dui sed, placerat ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Cras ante nisl, commodo a ex vitae, aliquet tempor purus. Nam eu ipsum sit amet justo vulputate luctus eu in ex. Sed mollis urna sit amet erat convallis feugiat. Proin convallis ipsum sed odio sodales, eget lacinia risus euisla ornare arcu id mauris suscipit, a consequat dui sollicitudin. Pellentesque maximus at urna vitae interdum. Fusce rutrum magna vel est facilisis imperdiet. Phasellus orci nisi, blandit non mollis luctus, sodales in velit. Quisque mattis tempor augue, eu blandit metus malesuada a. Nunc facilisis vel justo sit amet blandit. Etiam maximus nisi id purus finibus pulvinar non in nisi. Donec lacinia ligula a odio ornare, commodo iaculis libero rutrum. Suspendisse sodales enim sed mauris mollis, in suscipit ex mattis. In hac habitasse platea dictumst. Praesent aliquet, elit sit amet pharetra volutpat, metus odio porttitor magna, vitae egestas elit lorem rutrum velit. Mauris a accumsan nunc, vel convallissce facilisis massa eu mollis mollis. Proin pharetra maximus urna eu congue. Sed vel mi at enim vulputate ultrices eget et sem. Etiam ac metus iaculis est fringilla maximus. Vestibulum id elit eleifend dui placerat vestibulum. Phasellus est est, tristique sit amet dignissim nec, pulvinar et nisl. Curabitur eget lacus dolor. Suspendisse finibus hendrerit magna vulputate viverra. Ut luctus dui at risus elementum elemen porttitor tempus eros sit amet tempus. In vitae mauris gravida, ullamcorper dui sed, iaculis risus. Integer feugiat, velit ut volutpat blandit, justo est viverra elit, ut egestas quam lectus at massa. In hac habitasse platea dictumst. In vel dolor purus. Cras cursus odio in mi ullamcorper, et imperdiet arcu tempor. Sed vitae hendrerit nibh. Donec a vestibulum urna. Vestibulum viverra enim eu tellus aliquam dignissim. Proin iaculis massa eu ligula dapibus viverra. Praesent eget erat et leo lobortis euismod ut eu ante. Curabitur et laoreet quam. Etiam et tristique erat. Sed vel orci tempus, elementum sem ac, suscipit felis. Suspendisse iaculis eros et ante faucibus vehonec bibendum condimentum convallis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla porttitor nisl et posuere fermentum. Integer at tristique dui. Curabitur tempor vitae purus a vestibulum. Mauris imperdiet magna vel efficitur lobortis. Duis in dui aliquet, sagittis neque non, mollis purus. Ut vel dapibus risus. Nulla facilisi. Curabitur ut turpis ac urna porttitor vehicula at eu tellus. Nullam viverra purus tincidunt purus rutrum sollicitlla suscipit aliquet tincidunt. Mauris et neque enim. Aliquam non bibendum ante, vel mollis tellus. Nulla et mauris non metus sagittis cursus a sed urna. Ut ligula enim, malesuada et lorem in, ornare eleifend mi. Etiam sed sodales mauris. In a dui nec enim maximus sodales sit amet egestasonec vel massa vulputate, blandit ipsum eu, consectetur tortor. Vestibulum id cursus ex. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus posuere fringilla est. Donec sem lacus, condimentum nec pulvinar in, hendrerit sed justo. Fusce vitae auctor velit. Vivamus maximus nec augue at porttiin sodales augue mauris, nec finibus elit dignissim eu. Curabitur faucibus velit quam, at condimentum libero lacinia in. Vivamus elit metus, molestie eu mollis et, sollicitudin quis sapien. Sed commodo lorem non purus vestibulum viverra. Fusce commodo gravida dui ut dapibus. Praesent non neque rhoncus, finibus lectus sit amet, egestas odio. Fusce sapien velit, pellentesque ac erat ut, ultricies pulvinar drbi lorem leo, faucibus vel lacus at, aliquet mattis nibh. Proin ut ultricies quam. Vestibulum nec vulputate dui, in iaculis nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In hac habitasse platea dictumst. Ut ullamcorper magna diam, eget iaculis nisi tincidunt non. Nullam in magna non sapien consequat vulputate vel eget nulla. Curabitur eros erat, euismod vitae vestibulum ac, imperdiet eu ipsum. Morbi turpis arcu, consequat at lacinia eu, auctor sit amet maspendisse nec nibh dolor. Proin dignissim in odio et fermentum. Proin vitae iaculis ex, a tempus ligula. Cras eleifend justo at sodales sodales. Curabitur facilisis turpis ante, eu iaculis sapien euismod at. Pellentesque eu sem vel ante auctor euismod vitae in nisl. Quisque at condimentum odio. Nulla sed arcu quam. Nullam mattis dolor sed augue venenatis dictum. Nam eu rhoncus augue. Integer vel porttitor sapien. Ut non justo nibh. Vestibulum et lacus sit amet nulla sagittis tempus id vitae turpis. Vivamus congue magna massa, nec gravida quam sodales tincidunt. Integer nec enim sed ante viverra hendrerit. Vestibulum placerat convallis metus sed suscisque placerat varius elit, ut tincidunt eros. Duis bibendum a risus quis iaculis. Nullam placerat lectus non neque molestie eleifend. Cras eget nunc ut nunc fringilla consectetur eu et libero. Mauris nec sapien ac ante faucibus consequat tristique sit amet dolor. Mauris a semper odio. Vivamus sed orci est. Fusce sem urna, tincidunt id auctor ut, malesuada finibus nc semper non neque in vulputate. Duis eget ante ut ipsum tempor dignissim vitae a ex. Morbi consequat interdum nunc efficitur fringilla. Maecenas lectus tortor, tincidunt eu pretium id, elementum ac dolor. Duis id nisl massa. Aenean facilisis sem eu dolor ullamcorper, ac dictum purus semper. Quisque pellentesque leo vitae diam posuere rhoncus at nec dolor. In vestibulum, justo vel consequat blandit, elit enim rhoncus felis, laoreet consectetur ipsum nisi ut massa. Quisque tincidunt pellentesque diam, at ultricies ipsum tincidunt vitae. Pellentesque pulvinar congue felis id ultrices. Phasellus nec quam varius, varius elit non, finibus lectus. Duis sit amet bibendum augue. Phasellus euismod ex id egestas scelerisque. Maecenas accumsan lacus nec sem maximus, ac tempor ipsum feuglam at fermentum augue. In vehicula libero elit, id faucibus elit sollicitudin sed. Cras eu nisi aliquet, hendrerit elit in, pretium lacus. Quisque at egestas arcu, eu placerat velit. Nulla elementum, mi et finibus aliquam, velit enim placerat mi, sed viverra lacus magna nec dui. Donec id convallis elit, et placerat libero. Sed vel lectus non arcu viverra tempus. Nunc vel fringilla turpis. Suspendisse potenti. Aliquam vel metus nisl. Aenean in neque at quam ultricies aliquam sed vel libero. Sed lacinia turpis vitae porta aliqbi a aliquam dolor. Donec feugiat leo nunc, eu iaculis tortor imperdiet at. Duis et tincidunt tortor. Aenean at augue eget tortor tempor condimentum id at elit. Vestibulum quis tortor pretium, finibus diam id, maximus nisi. Cras elementum turpis quis est fringilla viverra. Quisque cursus sodales sem, id pellentesque dui interduam rhoncus ultrices lorem, at semper turpis tristique in. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean interdum dapibus risus at tincidunt. Duis urna elit, ultricies in lacus aliquet, dapibus dapibus nulla. Proin pellentesque venenatis fringilla. Ut efficitur pulvinar nibh vel convallis. In ac sollicitudin mi. Etiam bibendum feugiat nisi, nec lobortis magna aliquet vitae. Maecenas at pellentesque nulla. Etiam vulputate fringilla magna, a faucibus mauris rhoncus sit amet. Mauris fringilla augue non massa lacinia, sit amet porta eros ullamcorce sit amet nibh sed diam maximus gravida. In tellus ex, euismod euismod rutrum et, imperdiet at nisi. In nec mollis est, et fermentum nibh. Vivamus non consequat est. Integer tincidunt placerat sem, nec ultrices tellus interdum non. Fusce augue sem, tempus tincidunt eros non, egestas interdum nibh. Morbi eu pellentesque velit. Ut at risus erat. Ut egestas porta ex et euismod. Vestibulum nibh leo, mollis ut lobortis quis, sagittis sit amet nuec nec accumsan purus. Praesent pharetra condimentum purus, sed maximus turpis vestibulum dapibus. Sed facilisis turpis felis, et blandit leo ultrices quis. Vivamus placerat facilisis euismod. In quis enim nisi. Curabitur varius nisi et rhoncus tristique. Donec non ante gravida neque faucibus interdum at eu neque. Proin eu elit lacinia, dapibus purus a, faucibus turpis. Nunc vestibulum erat ac pellentesque lobortis. In hac habitasse platea dictumst. Donec sit amet leo dapibus, bibendum erat quis, tempus turpis. Duis semper quam eu lacus malesuada, eu consectetur erat luctus. Duis vehicula rutrum est, non viverra turpis commodo eu. Nam porta eu elit et fauciquam blandit eget elit vitae tempus. Mauris risus dui, dignissim eleifend fermentum at, tincidunt quis augue. Morbi in est varius, luctus metus pellentesque, ultrices lectus. Praesent in erat est. Aliquam rutrum mollis ante, ut vulputate augue fermentum a. Nunc id posuere tortor. In ut feugiat purus. Maecenas leo justo, mattis et odio in, maximus placerat diam. Fusce molestie, mauris quis semper dignissim, est neque ullamcorper lectus, sed commodo urna augue in justo. Sed viverra lacinia varius. Mauris felis sapien, iaculis id viverra nec, suscipit pharetra neque. Sed quis orci turpis. Nam sagittis lacinia ipsum et posuere. Donec nibh sapien, finibus id placerat vel, ornare id orci. Vestibulum aliquam at quam quis pharvamus sit amet posuere nulla. Donec vitae sapien posuere, pretium tortor eu, sollicitudin dui. Nullam vel auctor orci, in elementum sapien. Etiam vel maximus purus, et bibendum elit. Pellentesque pulvinar eleifend vestibulum. Aliquam euismod sodales risus sed ultricies. Duis rutrum ante quam, sed luctus eros elementum id. Praesent facilisis scelerisque tellus id finibus. Morbi id viverra dui. Nulla vehicula, nulla non congue tempor, nulla metus hendrerit ligula, ut lobortis tortor leo ut diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum eget tellus non nulla luctus ultrices nec non ex. Nullam feugiat placerat ipsum, interdum tincidunt tortor dictum sed. Morbi tincidunt auctor scelerillam dapibus, neque eu porttitor lobortis, orci risus eleifend tortor, venenatis porta elit leo id tortor. Praesent metus enim, lobortis in velit sit amet, fermentum semper libero. Donec et finibus arcu. Sed mattis mi sed dui aliquam feugiat. Phasellus non sem quis lorem pretium ultrices. Nunc vitae ligula congue nisi porttitor elementum. Suspendisse pharetra, tortor eu euismod mattis, velit elit laoreet lacus, at hendrerit metus risus ac purus. Maecenas molestie vitae nulla quis tristique. Pellentesque mauris ipsum, pharetra nec risus in, ultricies interdum veec mattis vel justo eu vehicula. Pellentesque iaculis ornare porttitor. Curabitur tempus mi sed metus vestibulum varius. Integer dictum ligula mi, in venenatis leo accumsan non. Proin viverra velit ut dolor rutrum volutpat. Morbi ac cursus enim, quis consequat ex. Vivamus iaculis imperdiet lectus non suscipit. Pellentesque porttitor quam at nunc ultricies tincidunt. Morbi a euismod nunc. Curabitur pellentesque ullamcorper auctor. Donec tempor, neque a maximus vehicula, dolor sem placerat mi, at tempus erat orci eu risus. Mauris ornare mattis mi, ac accumsan urna fringilla nec. Phasellus auctor imperdiet hendrelentesque semper pharetra orci, sed maximus ex. Suspendisse tortor erat, pulvinar non efficitur quis, feugiat ut odio. Cras ultricies pulvinar arcu eget scelerisque. In sollicitudin fermentum tincidunt. Etiam id sem nec arcu efficitur auctor id id ligula. Duis sit amet hendrerit tortor. Etiam interdum turpis sed mattis viverra. Sed imperdiet aliquam lorem vitae placerat. Donec pharetra nunc ut vulputate interdum. Morbi feugiat elit id venenatis egestas. Donec faucibus at leo in sagittis. Nunc eu vulputate turpis. In in mi ultrices, pharetra dui eget, feugiat velit. Integer egestas nisi sed velit varius, quis efficitur lorem ultrices. Pellentesque nec quam eget nulla euismod laoreet sit amet in est. ',
            # styles['Heading1'] 
        ))

        # Build the PDF document and add the page numbers
        doc.build(
            elements, 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response

    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        

        # Header customization
        header_text = 'REPORT TO BE PESENTED TO THE BOARD'
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)

        

        # # Add image in the header
        # img_path = 'http://uat.els.lgrb.go.ug/static/assets/img/brand/logo.png'  
        # img_width = 1.8 * inch
        # img_height = -0.6 * inch
        # img_x = doc.rightMargin + header_width - img_width
        # # img_y = header_y + (header_height - img_height) / 2
        # img_y = doc.height + doc.topMargin - img_height  # Pushed to the extreme top
        # # img = Image(img_path, width=img_width, height=img_height)
        # # img.drawOn(canvas, img_x, img_y)
        # img = ImageReader(img_path)
        # canvas.drawImage(img, img_x, img_y, img_width, img_height)

    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)


        # # Page number customization
        # page_number_text = f'Page {doc.page}'
        
        # page_number_style = ParagraphStyle(name='page_number', alignment=TA_CENTER)
        # page_number_width = doc.width - doc.leftMargin - doc.rightMargin
        # page_number_height = 0.2 * inch
        # page_number_x = doc.leftMargin
        # page_number_y = footer_y - page_number_height

        # footer = Paragraph(footer_text, footer_style)
        # footer.wrap(footer_width, footer_height)
        # footer.drawOn(canvas, footer_x, footer_y)

        # page_number = Paragraph(page_number_text, page_number_style)
        # page_number.wrap(page_number_width, page_number_height)
        # page_number.drawOn(canvas, page_number_x, page_number_y)


        # # Header
        # header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 1, styles['Normal'])
        # w, h = header.wrap(doc.width, doc.topMargin)
        # header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        #  # Add image in the footer
        # img_path = 'http://uat.els.lgrb.go.ug/static/assets/img/brand/logo.png'  # Replace with the actual image path
        # img_width = 1.5 * inch
        # img_height = 0.5 * inch
        # img_x = doc.leftMargin + footer_width - img_width
        # img_y = footer_y + (footer_height - img_height) / 2
        # img = Image(img_path, width=img_width, height=img_height)

        # img.drawOn(canvas, img_x, img_y)       

        # # Footer customization
        # footer_text = 'This is a custom footer.'
        # footer_style = styles['Normal']
        # footer_width = doc.width - doc.leftMargin - doc.rightMargin
        # footer_height = 0.5 * inch
        # footer_x = doc.leftMargin
        # footer_y = doc.bottomMargin - footer_height
        # footer = Paragraph(footer_text, footer_style)
        # footer.wrap(footer_width, footer_height)
        # footer.drawOn(canvas, footer_x, footer_y)

        # # Add image in the footer
        # img_path = 'http://uat.els.lgrb.go.ug/static/assets/img/brand/logo.png'  # Replace with the actual image path
        # img_width = 1.5 * inch
        # img_height = 0.5 * inch
        # img_x = doc.leftMargin + footer_width - img_width
        # img_y = footer_y + (footer_height - img_height) / 2
        # img = Image(img_path, width=img_width, height=img_height)

        # img.drawOn(canvas, img_x, img_y)

        # Release the canvas
        canvas.restoreState()



# Revenue combined
class PrincipleLicencerevenueView(View):

     template_name = 'reports/revenue/principle_licence_revenue.html'
     
     def get(self, request):
        
        context = {}

        revenues = PrincipleLicence.objects.all(
            # payment_description = "RECEIVED AND CREDITED",
            # payment_status = "T"
        )
        
        total_application_fees = PrincipleLicence.objects.values().annotate(
            total_amount = Sum ('application_fee'),
        )
  
       
        total_application_fees_per_company = PrincipleLicence.objects.all(
            # status='paid'
        ).values('name_of_the_company').annotate(
            total_amount=Sum('application_fee'),
            # total_employees = Sum('name_of_the_company')

        )

        total_application_fees_paid = PrincipleLicence.objects.all(
            # status='paid'
        ).aggregate(total_amount=Sum('licence_fee'))


        total_licence_fees_per_company = PrincipleLicence.objects.all(
            # status='paid'
        ).values('name_of_the_company').annotate(
            total_amount=Sum('licence_fee'),
            # total_employees = Sum('name_of_the_company')

        )

        total_licence_fees_paid = PrincipleLicence.objects.all(
            # status='paid'
        ).aggregate(total_amount=Sum('application_fee'))


        
        totoal_payments = [ total_application_fees_paid, total_licence_fees_paid  ]

        context['totoal_payments'] = totoal_payments 

        context['total_licence_fees_per_company'] = total_licence_fees_per_company
        context['total_licence_fees_paid'] = total_licence_fees_paid

        context['total_application_fees_per_company'] = total_application_fees_per_company
        context['total_application_fees_paid'] = total_application_fees_paid
        
        context['total_application_fees'] = total_application_fees
        # context['sum_per_company'] = sum_per_company
        context['revenues'] = revenues

        return render(request, self.template_name, context)


class PremiseLicenceRevenueView(View):

     template_name = 'reports/revenue/premise_licence_revenue.html'
     
     def get(self, request):
        
        context = {}
        

        # amounts 

        total_inspection_fees_paid = PremiseLicence.objects.all(
            # status='paid'
        ).aggregate(total_amount=Sum('inspection_fee'))

        total_inspection_fees_per_company = PremiseLicence.objects.all(
            # status='paid'
        ).values('operator_name').annotate(
            total_amount=Sum('inspection_fee'),
            total_premises = Count('id')
            
        )

        # premises based on the regions 

        region_counts = PremiseLicence.objects.values('region').annotate(count=Count('id'))

        context['region_counts'] = region_counts

        context['total_inspection_fees_paid'] = total_inspection_fees_paid
        context['total_inspection_fees_per_company'] = total_inspection_fees_per_company
        context['totoal_payments'] =  [ total_inspection_fees_paid, total_inspection_fees_paid  ] 

        return render(request, self.template_name, context) 

 
class EmployeeLicenceRevenueView(View):

     template_name = 'reports/revenue/employee_licence_revenue.html'
     
     def get(self, request):
        
        context = {}
        
        # amounts 

        total_inspection_fees_paid = EmployeeLicence.objects.all(
            # status='paid'
        ).aggregate(total_amount=Sum('application_fee'))

        total_inspection_fees_per_company = EmployeeLicence.objects.all(
            # status='paid'
        ).values('name_of_the_company').annotate(
            total_amount=Sum('application_fee'),
            total_premises = Count('id')
            
        )

        # premises based on the regions 

        employee_count = EmployeeLicence.objects.values('name_of_the_company').annotate(count=Count('id'))

        context['employee_count'] = employee_count

        context['total_inspection_fees_paid'] = total_inspection_fees_paid
        context['total_inspection_fees_per_company'] = total_inspection_fees_per_company
        context['totoal_payments'] =  [ total_inspection_fees_paid, total_inspection_fees_paid  ] 

        return render(request, self.template_name, context) 


class ApprovalReportView(View):

    template_name = 'reports/revenue/employee_licence_revenue.html'
    approval_form = ApprovalForm
    
    def get(self, request):
        
        context = {}
        context['approval_form'] = self.approval_form
        
        # amounts 

        total_inspection_fees_paid = EmployeeLicence.objects.all(
            # status='paid'
        ).aggregate(total_amount=Sum('application_fee'))

        total_inspection_fees_per_company = EmployeeLicence.objects.all(
            # status='paid'
        ).values('name_of_the_company').annotate(
            total_amount=Sum('application_fee'),
            total_premises = Count('id')
            
        )

        # premises based on the regions 

        employee_count = EmployeeLicence.objects.values('name_of_the_company').annotate(count=Count('id'))

        context['employee_count'] = employee_count

        context['total_inspection_fees_paid'] = total_inspection_fees_paid
        context['total_inspection_fees_per_company'] = total_inspection_fees_per_company
        context['totoal_payments'] =  [ total_inspection_fees_paid, total_inspection_fees_paid  ] 

        return render(request, self.template_name, context) 
    

class AllEmployees(View):

    def get(self, request, *args, **kwargs):

        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        custom_page_size = landscape(letter)
       
        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 

            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
           
            topMargin=72,
            bottomMargin=60,
            pagesize=custom_page_size
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = PremiseLicence.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        Spacer(1, 14)
        elements.append(
            Paragraph( 'APPROVED KEY EMPLOYEES LICENCES. ' ,
            styles['Heading1'] 
        ))

        Spacer(width=0, height=23.5) 


        premises  = EmployeeLicence.objects.all().values_list(
            'name_of_the_company', 'name_of_the_employee', 'occupation', 'licence_number', 'prn', 'payment_description', 'approving_authority_remarks',
        )
        # Create the table for user details
        premise_table_data = [['Company Name', 'Employee name', 'Designation / Employee position', 'Licence Number', 'PRN', 'Payment', 'Comments']]
        premise_table_data.extend(premises)
        premise_table = Table(premise_table_data)
        premise_table.setStyle(TableStyle([
            # Table style settings
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        
        ('FONTSIZE', (0,0), (-1,-1), 8),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        # ('FONTSIZE', (0,0), (-1,0), 5),
        # ('BOTTOMPADDING', (0,0), (-1,0), 12),
        # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        # ('FONTSIZE', (0,1), (-1,-1), 12),
        # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
        # ('BOTTOMPADDING', (0,1), (-1,-1), 6),
           
        ]))

        
        # Add paragraph describing the user table
        premise_table_description = "Bellow are a list of all employees  which has bee approved as of 12/03/2023. "
        elements.append(Paragraph(premise_table_description, styles['Normal']))
        elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
        elements.append(premise_table)

        

        # elements.append(
        #     Paragraph('Lorem sed felis. tellus tempus laoreet. Sed at quam arcu. In gravida justo elit, nec rhoncus ligula vehicula vel. Quisque et mauris non felis venenatis faucibus at leo in sagittis. Nunc eu vulputate turpis. In in mi ultrices, pharetra dui eget, feugiat velit. Integer egestas nisi sed velit varius, quis efficitur lorem ultrices. Pellentesque nec quam eget nulla euismod laoreet sit amet in est. ',
        # ))

        # Build the PDF document and add the page numbers
        doc.build(
            elements,
            # [table], 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response
        # add the nuber as an id to the licence 

    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Header customization
        header_text = ''
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)
    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)

        # Release the canvas
        canvas.restoreState()


class AllPrincipleLicences(View):


    def get(self, request, *args, **kwargs):

        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        custom_page_size = landscape(letter)
    
        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 

            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
           
            topMargin=72,
            bottomMargin=60,
            pagesize=custom_page_size
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = PremiseLicence.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        Spacer(1, 14)
        elements.append(
            Paragraph( 'APPROVED PRINCIPLE LICENCES. ' ,
            styles['Heading1'] 
        ))

        Spacer(width=0, height=23.5) 

        premises  = PrincipleLicence.objects.all().values_list(
            'name_of_the_company', 'licence_type', 'prn', 'payment_description', 'approving_authority_status',
        ).order_by('name_of_the_company')
        # Create the table for user details
        premise_table_data = [['Company Name', 'Licence type', 'PRN', 'Licence Number', 'PRN', 'Payment', 'Comments']]
        premise_table_data.extend(premises)
        premise_table = Table(premise_table_data)
        premise_table.setStyle(TableStyle([
            # Table style settings
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        
        ('FONTSIZE', (0,0), (-1,-1), 8),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        # ('FONTSIZE', (0,0), (-1,0), 5),
        # ('BOTTOMPADDING', (0,0), (-1,0), 12),
        # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        # ('FONTSIZE', (0,1), (-1,-1), 12),
        # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
        # ('BOTTOMPADDING', (0,1), (-1,-1), 6),
           
        ]))

        
        # Add paragraph describing the user table
        premise_table_description = "Bellow are a list of all employees  which has bee approved as of 12/03/2023. "
        elements.append(Paragraph(premise_table_description, styles['Normal']))
        elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
        elements.append(premise_table)

        

        # elements.append(
        #     Paragraph('Lorem sed felis. tellus tempus laoreet. Sed at quam arcu. In gravida justo elit, nec rhoncus ligula vehicula vel. Quisque et mauris non felis venenatis malesuada ac et urna.  ',
        # ))

        # Build the PDF document and add the page numbers
        doc.build(
            elements,
            # [table], 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response
        # add the nuber as an id to the licence 


    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Header customization
        header_text = ''
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)
    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)

        # Release the canvas from the page 

        canvas.restoreState()


# principle 

class PrincipleApprovalsView(View):

    template_name = "reports/report/principle_approval_report.html"
    approval_form = ApprovalForm

    def get(self, request, *args, **kwargs):
        context = {}
        context['approval_form'] = self.approval_form 

        return render(request, self.template_name, context )


class AllPrinciplePdfReport(View):

    def get(self, request, *args, **kwargs):

        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        custom_page_size = landscape(letter)
        
        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 

            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
           
            topMargin=72,
            bottomMargin=60,
            pagesize=custom_page_size
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = PrincipleLicence.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        Spacer(1, 14)

        approval_status = request.GET.get('approval_status')

        premises = PrincipleLicence.objects.filter( approving_authority_status=approval_status ).values_list(
            'name_of_the_company', 'licence_type', 'date_applied', 'applicationfeepayments__prn', 'approving_authority_status',
        ).prefetch_related('applicationfeepayments')
        licence_status = str(premises[0][2]).upper()
        date_generated = date.today()

        # Create the table for user details
        premise_table_data = [['Company Name', 'Licence Type', 'Date applied', 'Payment', 'Comments']]

        elements.append(
            Paragraph( f'{licence_status} PREMISE LICENCES. ' ,
            styles['Heading1'] 
        ))

        premise_table_data.extend(premises)
        premise_table = Table(premise_table_data)
        premise_table.setStyle(TableStyle([
            # Table style settings
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        
        ('FONTSIZE', (0,0), (-1,-1), 8),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        # ('FONTSIZE', (0,0), (-1,0), 5),
        # ('BOTTOMPADDING', (0,0), (-1,0), 12),
        # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        # ('FONTSIZE', (0,1), (-1,-1), 12),
        # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
        # ('BOTTOMPADDING', (0,1), (-1,-1), 6),
           
        ]))
       
        Spacer(width=0, height=23.5) 

        # Add paragraph describing the user table
        premise_table_description = f"Bellow are a list of all premises  which has been {licence_status} as of {date_generated}. "

        elements.append(Paragraph(premise_table_description, styles['Normal']))
        elements.append(premise_table)
        elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
        
        # Build the PDF document and add the page numbers
        doc.build(
            elements,
            # [table], 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response
    

    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Header customization
        header_text = ''
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)
    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)

        # Release the canvas
        canvas.restoreState()


class AllPrincipleCsvReport(View):

    def get(self, request, *args, **kwargs):

        # Create a file-like buffer to receive CSV data
        buffer = StringIO()
        
        writer = csv.writer(buffer)

        # Write header row
        header = ['Company Name', 'Licence Type', 'Date applied', 'Payment', 'Comments']
        writer.writerow(header)

        # Fetch premises data
        premises = PrincipleLicence.objects.filter(approving_authority_status="Approved").values_list(
            'name_of_the_company', 'licence_type', 'date_applied', 'applicationfeepayments__prn', 'approving_authority_status',
        ).prefetch_related('applicationfeepayments')

        # Write premises data rows
        for row in premises:
            writer.writerow(row)

        # Generate response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="premises.csv"'

        # Retrieve the CSV contents from the buffer and write it to the response
        response.write(buffer.getvalue())

        return response

# employee
class EmployeeApprovalsView(View):

    template_name = "reports/report/employee_approval_report.html"
    form_class = EmployeeFilterForm
    year_form = YearFilterForm
    verification_form = VerificationRecomendationForm
    
    def get(self, request, *args, **kwargs):

        context = {}

        context['form'] = self.form_class
        context['year_form'] = self.year_form 
        context['verification_form'] = self.verification_form


        if request.method == 'GET':

            year = request.GET.get('year')

            if year:

                records = PrincipleLicence.objects.filter(date_applied__year=year)
                pie_data = records.values('village').annotate(count=Count('village'))
                bar_data = records.values('approved').annotate(count=Count('approved'))
                doughnut_data = records.values('email').annotate(count=Count('email'))

                pie_data_json = json.dumps(list(pie_data), cls=jencoder)
                bar_data_json = json.dumps(list(bar_data), cls=jencoder)
                doughnut_data_json = json.dumps(list(doughnut_data), cls=jencoder)

                print(doughnut_data_json)

                context['pie_data'] =  pie_data_json,
                context['bar_data'] =  bar_data_json,
                context['doughnut_data'] =  doughnut_data_json
            
        return render(request, self.template_name, context)
    

class AllEmployeesPdfReport(View):

    def get(self, request, *args, **kwargs):


        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        custom_page_size = landscape(letter)
        

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 

            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
           
            topMargin=72,
            bottomMargin=60,
            pagesize=custom_page_size
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = PremiseLicence.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        Spacer(1, 14)

        approval_status = request.GET.get('approval_status')
        # year = request.GET.get('year')

        employees  = EmployeeLicence.objects.filter(
            # date_applied__year = year, 
            approving_authority_status=approval_status
        ).values_list(
            'name_of_the_company', 'name_of_the_employee', 'occupation', 'licence_number', 'prn', 'payment_description', 'approving_authority_remarks',
        )

        employees_table_data = [['Company Name', 'Employee name', 'Designation / Employee position', 'Licence Number', 'PRN', 'Payment', 'Comments']]

        # licence_status = str(employees[0][6]).upper()
        date_generated = date.today()

        # elements.append(
        #     Paragraph( f'{licence_status} PREMISE LICENCES ' ,
        #     styles['Heading1'] 
        # ))

        employees_table_data.extend(employees)
        premise_table = Table(employees_table_data)
        premise_table.setStyle(TableStyle([
            # Table style settings
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        
        ('FONTSIZE', (0,0), (-1,-1), 8),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        # ('FONTSIZE', (0,0), (-1,0), 5),
        # ('BOTTOMPADDING', (0,0), (-1,0), 12),
        # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        # ('FONTSIZE', (0,1), (-1,-1), 12),
        # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
        # ('BOTTOMPADDING', (0,1), (-1,-1), 6),
           
        ]))
       
        Spacer(width=0, height=23.5) 

        # Add paragraph describing the user table
        premise_table_description = f"Bellow are a list of all employees  which has been as of {date_generated}. "

        elements.append(Paragraph(premise_table_description, styles['Normal']))
        elements.append(premise_table)
        elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
        
        # Build the PDF document and add the page numbers
        doc.build(
            elements,
            # [table], 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response
    

    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Header customization
        header_text = ''
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)
    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)

        # Release the canvas
        canvas.restoreState()


class EmployeeByCompanyPdfReport(View):

        def get(self, request, *args, **kwargs):


            '''
            # amounts 
            total_inspection_fees_paid = EmployeeLicence.objects.filter(
                # status='paid'
            ).aggregate(total_amount=Sum('application_fee'))
            total_inspection_fees_per_company = EmployeeLicence.objects.all(
                # status='paid'
            ).values('name_of_the_company').annotate(
                total_amount=Sum('application_fee'),
                total_premises = Count('id')
                
            )
            # premises based on the regions 
            employee_count = EmployeeLicence.objects.values('name_of_the_company').annotate(count=Count('id'))
            '''

            # Create a file-like buffer to receive PDF data.
            buffer = BytesIO()

            custom_page_size = landscape(letter)
            

            # Create the PDF object, using the buffer as its "file."
            doc = SimpleDocTemplate(
                buffer, 

                leftMargin=0.5 * inch,
                rightMargin=0.5 * inch,
            
                topMargin=72,
                bottomMargin=60,
                pagesize=custom_page_size
            )

            # Our container for 'Flowable' objects
            elements = []

            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

            # styles = getSampleStyleSheet()
            # title_style = styles['Heading1']
            # title_style.alignment = 1
            # title_style.fontSize = 30

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            users = PremiseLicence.objects.all()
            # elements.append(Paragraph('Approved Licence Report' ))
            # elements.append(Paragraph('Approved Licence Report', title_style ))

            Spacer(1, 14)


            # top table 


            name_of_the_company = request.GET.get('name_of_the_company')
            employees  = EmployeeLicence.objects.filter(email=name_of_the_company).values_list(
                'name_of_the_company', 'name_of_the_employee', 'occupation', 'licence_number', 'prn', 'payment_description', 'approving_authority_remarks',
            )
            employees_table_data = [['Company Name', 'Employee name', 'Designation / Employee position', 'Licence Number', 'PRN', 'Payment', 'Comments']]

            # company = str(employees[0][4]).upper()
            date_generated = date.today()

            # elements.append(
            #     Paragraph( f'{company} EMPLOYEES LICENCES ' ,
            #     styles['Heading1'] 
            # ))

            employees_table = [ ['Company Name' ], ['Licence type'] ]
            employees_table_data.extend(employees)
            premise_table = Table(employees_table)
            premise_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.blue),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
                # ('FONTSIZE', (0,0), (-1,0), 5),
                # ('BOTTOMPADDING', (0,0), (-1,0), 12),
                # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
                # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                # ('FONTSIZE', (0,1), (-1,-1), 12),
                # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
                # ('BOTTOMPADDING', (0,1), (-1,-1), 6)
            ]))
            elements.append(premise_table)
            elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs


            employees_table_data.extend(employees)
            premise_table = Table(employees_table_data)
            premise_table.setStyle(TableStyle([
                # Table style settings
                ('BACKGROUND', (0,0), (-1,0), colors.green),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
                # ('FONTSIZE', (0,0), (-1,0), 5),
                # ('BOTTOMPADDING', (0,0), (-1,0), 12),
                # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
                # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                # ('FONTSIZE', (0,1), (-1,-1), 12),
                # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
                # ('BOTTOMPADDING', (0,1), (-1,-1), 6),    
            ]))
        
            Spacer(width=0, height=23.5) 

            # Add paragraph describing the user table
            premise_table_description = f"Bellow are a list of all employees  of  as of {date_generated}. "

            elements.append(Paragraph(premise_table_description, styles['Normal']))
            elements.append(premise_table)
            elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
            
            # Build the PDF document and add the page numbers
            doc.build(
                elements,
                onFirstPage=self._header_footer, 
                onLaterPages=self._header_footer,
                canvasmaker=NumberedCanvas
            )

            # Get the value of the BytesIO buffer and return the PDF as a response.
            pdf = buffer.getvalue()
            buffer.close()

            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
            response.write(pdf)
            return response
    
        @staticmethod
        def _header_footer(canvas, doc):

            # Save the state of our canvas so we can draw on it
            canvas.saveState()
            styles = getSampleStyleSheet()
            
            # Header customization
            header_text = ''
            header_style = styles['Normal']
            header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
            header_width = doc.width - doc.leftMargin - doc.rightMargin
            header_height = 0.1 * inch
            header_height = 0.2 * inch
            header_x = doc.leftMargin
            header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
            header = Paragraph(header_text, header_style)
            header.wrap(header_width, header_height)
            header.drawOn(canvas, header_x, header_y)
        
            # Footer customization
            footer_text = ''
            footer_style = styles['Normal']
            footer_width = doc.width - doc.leftMargin - doc.rightMargin
            footer_height = 0.5 * inch
            footer_x = doc.leftMargin
            footer_y = doc.bottomMargin - footer_height
            footer = Paragraph(footer_text, footer_style)
            footer.wrap(footer_width, header_height)
            footer.drawOn(canvas, footer_x, footer_y)

            # Release the canvas
            canvas.restoreState()


class AllRecomenedEmployeesPdfReport(View):

    def get(self, request, *args, **kwargs):

        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        custom_page_size = landscape(letter)

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 

            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
           
            topMargin=72,
            bottomMargin=60,
            pagesize=custom_page_size
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = PremiseLicence.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        Spacer(1, 14)

        verification_status = request.GET.get('verification_status')
        year = request.GET.get('year')

        employees  = EmployeeLicence.objects.filter(
            date_applied__year = year, 
            approving_authority_status=verification_status
        ).values_list(
            'name_of_the_company', 'name_of_the_employee', 'occupation', 'licence_number', 'prn', 'payment_description', 'approving_authority_remarks',
        )

        employees_table_data = [['Company Name', 'Employee name', 'Designation / Employee position', 'Licence Number', 'PRN', 'Payment', 'Comments']]

        # licence_status = str(employees[0][6]).upper()
        date_generated = date.today()

        # elements.append(
        #     Paragraph( f'{licence_status} PREMISE LICENCES ' ,
        #     styles['Heading1'] 
        # ))

        employees_table_data.extend(employees)
        premise_table = Table(employees_table_data)
        premise_table.setStyle(TableStyle([
            # Table style settings
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        
        ('FONTSIZE', (0,0), (-1,-1), 8),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        # ('FONTSIZE', (0,0), (-1,0), 5),
        # ('BOTTOMPADDING', (0,0), (-1,0), 12),
        # ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        # ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        # ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        # ('FONTSIZE', (0,1), (-1,-1), 12),
        # ('VALIGN', (0,1), (-1,-1), 'MIDDLE'),
        # ('BOTTOMPADDING', (0,1), (-1,-1), 6),
           
        ]))
       
        Spacer(width=0, height=23.5) 

        # Add paragraph describing the user table
        premise_table_description = f"Bellow are a list of all employees  which has been as of {date_generated}. "

        elements.append(Paragraph(premise_table_description, styles['Normal']))
        elements.append(premise_table)
        elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
        
        # Build the PDF document and add the page numbers
        doc.build(
            elements,
            # [table], 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response
    

    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Header customization
        header_text = ''
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)
    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)

        # Release the canvas
        canvas.restoreState()


# premise licence 

class PremiseApprovalsView(View):

    template_name = "reports/report/premise_approval_report.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


class AllPremisesPdfReport(View):

    def get(self, request, *args, **kwargs):

    
        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        custom_page_size = landscape(letter)
        

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(
            buffer, 

            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
           
            topMargin=72,
            bottomMargin=60,
            pagesize=custom_page_size
        )

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # styles = getSampleStyleSheet()
        # title_style = styles['Heading1']
        # title_style.alignment = 1
        # title_style.fontSize = 30

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = PremiseLicence.objects.all()
        # elements.append(Paragraph('Approved Licence Report' ))
        # elements.append(Paragraph('Approved Licence Report', title_style ))

        Spacer(1, 14)

        approval_status = request.GET.get('approval_status')

        premises = PremiseLicence.objects.filter( approving_authority_status=approval_status ).values_list(
            'operator_name', 'trade_name', 'premise_name', 'region', 'district', 'municipality', 'town_council', 'payment_description', 'approving_authority_status',
        )

        licence_status = str(premises[0][8]).upper()
        date_generated = date.today()

        # Create the table for user details
        premise_table_data = [['Operator Name', 'Trade name', 'Premise name', 'Region', 'District', 'Municipality', 'Town council', 'Payment', 'Comments']]

        elements.append(
            Paragraph( f'{licence_status} PREMISE LICENCES. ' ,
            styles['Heading1'] 
        ))

        premise_table_data.extend(premises)
        premise_table = Table(premise_table_data)
        premise_table.setStyle(TableStyle([
            # Table style settings
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        
        ('FONTSIZE', (0,0), (-1,-1), 8),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
       
           
        ]))
       
        Spacer(width=0, height=23.5) 

        # Add paragraph describing the user table
        premise_table_description = f"Bellow are a list of all premises  which has been {licence_status} as of {date_generated}. "

        elements.append(Paragraph(premise_table_description, styles['Normal']))
        elements.append(premise_table)
        elements.append(Spacer(1, 10))  # Spacer for spacing between paragraphs
        
        # Build the PDF document and add the page numbers
        doc.build(
            elements,
            # [table], 
            onFirstPage=self._header_footer, 
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )

        # Get the value of the BytesIO buffer and return the PDF as a response.
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="users.pdf"'
        response.write(pdf)
        return response
    

    @staticmethod
    def _header_footer(canvas, doc):

        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        # Header customization
        header_text = ''
        header_style = styles['Normal']
        header_style = ParagraphStyle(name='header', alignment=TA_CENTER)
        header_width = doc.width - doc.leftMargin - doc.rightMargin
        header_height = 0.1 * inch
        header_height = 0.2 * inch
        header_x = doc.leftMargin
        header_y = doc.height + doc.topMargin - header_height - 0.1 * inch  # Adjust the margin as desired
        header = Paragraph(header_text, header_style)
        header.wrap(header_width, header_height)
        header.drawOn(canvas, header_x, header_y)
    
        # Footer customization
        footer_text = ''
        footer_style = styles['Normal']
        footer_width = doc.width - doc.leftMargin - doc.rightMargin
        footer_height = 0.5 * inch
        footer_x = doc.leftMargin
        footer_y = doc.bottomMargin - footer_height
        footer = Paragraph(footer_text, footer_style)
        footer.wrap(footer_width, header_height)
        footer.drawOn(canvas, footer_x, footer_y)

        # Release the canvas
        canvas.restoreState()



def dasboards(request):

    if request.method == 'GET':
        year = request.GET.get('year')

        if year:
            records = PrincipleLicence.objects.filter(date__year=year)
            pie_data = records.values('approval_status').annotate(count=Count('approval_status'))
            bar_data = records.values('month').annotate(count=Count('month'))
            doughnut_data = records.values('status').annotate(count=Count('status'))

            pie_data_json = json.dumps(list(pie_data), cls=json.JsonEncoder)
            bar_data_json = json.dumps(list(bar_data), cls=json.JsonEncoder)
            doughnut_data_json = json.dumps(list(doughnut_data), cls=json.JsonEncoder)

            return render(request, 'graphs.html', {
                'pie_data': pie_data_json,
                'bar_data': bar_data_json,
                'doughnut_data': doughnut_data_json
            })

    return render(request, 'graphs.html')