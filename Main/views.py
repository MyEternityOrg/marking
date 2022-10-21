from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView, TemplateView
from django.views.generic.edit import BaseFormView, UpdateView

from Marking.mixin import *
from .models import *
from .forms import *
from .filters import *


class IndexPageFormView(BaseClassContextMixin, TemplateView):
    title = 'Система маркировки'
    template_name = 'Main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageFormView, self).get_context_data(**kwargs)
        # context['tests'] = ModelDocuments.objects.values('contractor_guid').annotate(count=Count('contractor_guid'))
        return context


class DocumentsListView(BaseClassContextMixin, ListView):
    title = 'Система маркировки - УПД'
    template_name = 'Main/document_list_universal.html'
    model = ModelDocuments
    paginate_by = 30

    def __init__(self, **kwargs):
        super(DocumentsListView, self).__init__(**kwargs)
        self.filter_set = None

    def get_context_data(self, **kwargs):
        context = super(DocumentsListView, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        f = context['filter'].data
        context[
            'filtered_path'] = f"?document_date_after={f.get('document_date_after', '')}&" \
                               f"document_date_before={f.get('document_date_before', '')}&" \
                               f"contractor_guid={f.get('contractor_guid', '')}&" \
                               f"document_status_id={f.get('document_status_id', '')}"
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
    paginate_by = 100
    title = 'Контрагенты'


class SprtCisStatusesListView(BaseClassContextMixin, ListView):
    model = ModelCisStatuses
    template_name = 'Main/sprt_list_cis_statuses.html'
    paginate_by = 100
    title = 'Статусы КИЗ/КИТУ'


class SprtDocumentStatusesListView(BaseClassContextMixin, ListView):
    model = ModelDocumentStatuses
    template_name = 'Main/sprt_list_document_statuses.html'
    paginate_by = 100
    title = 'Статусы проверки документов'


class SprtWaresListView(BaseClassContextMixin, ListView):
    model = ModelWares
    template_name = 'Main/sprt_list_wares.html'
    paginate_by = 200
    title = 'Номенклатура'

    def __init__(self, **kwargs):
        super(SprtWaresListView, self).__init__(**kwargs)
        self.filter_set = None

    def get_context_data(self, **kwargs):
        context = super(SprtWaresListView, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        f = context['filter'].data
        context['filtered_path'] = f"?ware_code={f.get('ware_code', '')}&" \
                                   f"ware_name={f.get('ware_name', '')}&" \
                                   f"marked={f.get('marked', False)}"
        return context

    def get_queryset(self):
        query_set = ModelWares.get_records()
        data = self.request.GET
        if data == {}:
            data = {'marked': False}
        self.filter_set = FilterWares(data, queryset=query_set)
        return self.filter_set.qs


class SprtContractorUpdateView(UpdateView, BaseClassContextMixin):
    title = 'Обновить данные контрагента'
    model = ModelContractors
    template_name = 'Main/spt_update_contractors.html'
    form_class = FormContractor
    success_url = reverse_lazy('Main:contractors')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.model.objects.get(contractor_guid=self.kwargs.get('pk')))
        if form.is_valid():
            data = form.save()
        return redirect(self.success_url)
