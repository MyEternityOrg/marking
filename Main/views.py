from django.shortcuts import render
from django.views.generic import FormView, DetailView, ListView
from django.views.generic.edit import BaseFormView

from Marking.mixin import *
from .models import *
from .forms import *


class IndexPageFormView(BaseClassContextMixin, ListView):
    title = 'Система маркировки'
    template_name = 'Main/index.html'
    model = ModelDocuments
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(IndexPageFormView, self).get_context_data(**kwargs)
        return context
