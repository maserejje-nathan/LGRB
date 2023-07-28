from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from rest_framework import routers


from api.views import *

# swagger-ui imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="LGRB ELS API",
      default_version='v1',
      description="National Lottery and Gaming Regulartory Board Electronic licencing  System API",
      terms_of_service="https://www.uat.els.lgrb.go.ug/",
      contact=openapi.Contact(email="daniel.okot@nita.go.ug"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('client.urls')),
    path('', include('administrator.urls' )),
    path('', include('account.urls')),
    path('', include('new.urls')),
    path('', include('bankguarantee.urls' )),
    path('', include('payments.urls' )),
    path('', include('reports.urls' )),
    path('', include('api.urls')),



    # swagger-ui api documentation
    path('api/v1/', include([
       path('api/api.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
       path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
       path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ])),

    # rest framework provider
    path('api-auth/', include('rest_framework.urls')),

    # oauth provider
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
]

urlpatterns +=staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)