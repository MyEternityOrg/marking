from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView
from django.views.generic.edit import BaseFormView

from Marking.mixin import *
from .models import *
from .forms import *
from .filters import *


class IndexPageFormView(BaseClassContextMixin, ListView):
    title = 'Система маркировки'
    template_name = 'Main/index.html'
    model = ModelDocuments
    paginate_by = 25

    def __init__(self, **kwargs):
        super(IndexPageFormView, self).__init__(**kwargs)
        self.filter_set = None

    def get_context_data(self, **kwargs):
        context = super(IndexPageFormView, self).get_context_data(**kwargs)
        context['filter'] = self.filter_set
        context[
             'filtered_path'] = f"?document_date_after={self.request.GET.get('document_date_after', '')}&document_date_before={self.request.GET.get('document_date_before', '')}&contractor_guid={self.request.GET.get('contractor_guid', '')}"
        return context

    def get_queryset(self):
        query_set = self.model.objects.all()
        dts = datetime.date.today().strftime('%Y-%m-%d')
        data = self.request.GET
        if data == {}:
            data = {'document_date_after': dts, 'document_date_before': dts}
        self.filter_set = FilterDocumentsList(data, queryset=query_set)
        return self.filter_set.qs
