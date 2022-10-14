from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from .views import *

app_name = 'Main'

urlpatterns = [
    path('', IndexPageFormView.as_view(), name='index'),
    path('documents/search/', DocumentsListView.as_view(), name='documents'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
