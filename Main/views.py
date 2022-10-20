from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView, TemplateView
from django.views.generic.edit import BaseFormView

from Marking.mixin import *
from .models import *
from .forms import *
from .filters import *


class IndexPageFormView(BaseClassContextMixin, TemplateView):
    title = 'Система маркировки'
    template_name = 'Main/index.html'


class DocumentsListView(BaseClassContextMixin, ListView):
    title = 'Система маркировки - УПД'
    template_name = 'Main/document_list_universal.html'
    model = ModelDocuments
    paginate_by = 25

    def __init__(self, **kwargs):
        super(DocumentsListView, self).__init__(**kwargs)
        self.filter_set = None

    def get_context_data(self, **kwargs):
        context = super(DocumentsListView, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        context[
            'filtered_path'] = f"?document_date_after={self.request.GET.get('document_date_after', '')}&" \
                               f"document_date_before={self.request.GET.get('document_date_before', '')}&" \
                               f"contractor_guid={self.request.GET.get('contractor_guid', '')}"
        return context

    def get_queryset(self):
        query_set = self.model.objects.all()
        dts = datetime.date.today().strftime('%Y-%m-%d')
        data = self.request.GET
        if data == {}:
            data = {'document_date_after': dts, 'document_date_before': dts}
        self.filter_set = FilterDocumentsList(data, queryset=query_set)
        return self.filter_set.qs


class SprtContractorsListView(BaseClassContextMixin, ListView):
    model = ModelContractors
    template_name = 'Main/sprt_list_contractors.html'
    paginate_by = 30
    title = 'Контрагенты'


class SprtCisStatusesListView(BaseClassContextMixin, ListView):
    model = ModelCisStatuses
    template_name = 'Main/sprt_list_cis_statuses.html'
    paginate_by = 30
    title = 'Статусы КИЗ/КИТУ'


class SprtDocumentStatusesListView(BaseClassContextMixin, ListView):
    model = ModelDocumentStatuses
    template_name = 'Main/sprt_list_document_statuses.html'
    paginate_by = 30
    title = 'Статусы проверки документов'


class SprtWaresListView(BaseClassContextMixin, ListView):
    model = ModelWares
    template_name = 'Main/sprt_list_wares.html'
    paginate_by = 30
    title = 'Номенклатура'

    def __init__(self, **kwargs):
        super(SprtWaresListView, self).__init__(**kwargs)
        self.filter_set = None

    def get_context_data(self, **kwargs):
        context = super(SprtWaresListView, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        context['filtered_path'] = f"?ware_code={self.request.GET.get('ware_code', '')}"
        return context

    def get_queryset(self):
        query_set = ModelWares.get_records()
        self.filter_set = FilterWares(self.request.GET, queryset=query_set)
        return self.filter_set.qs
