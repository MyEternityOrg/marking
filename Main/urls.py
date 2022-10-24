from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from .views import *

app_name = 'Main'

urlpatterns = [
    path('', IndexPageFormView.as_view(), name='index'),
    path('documents/', DocumentsListView.as_view(), name='documents'),
    path('sprt/contractors/', SprtContractorsListView.as_view(), name='contractors'),
    path('sprt/contractors/save_contractor_data/', save_contractor_data, name='save_contractor_data'),
    path('sprt/contractors/modify/<pk>', SprtContractorUpdateView.as_view(), name='contractors_record'),
    path('sprt/cis_statuses/', SprtCisStatusesListView.as_view(), name='cis_statuses'),
    path('sprt/documents_statuses/', SprtDocumentStatusesListView.as_view(), name='document_statuses'),
    path('sprt/wares/', SprtWaresListView.as_view(), name='wares'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
