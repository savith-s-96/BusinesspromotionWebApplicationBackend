
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view
def index(request) :
      
      return Response({"message" : "Locito Api Welcomes you"})

urlpatterns = [
    path("",index),
    path('admin/', admin.site.urls),
    path("api/",include("LocitoApi.urls")),
]

if settings.DEBUG :

      urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
