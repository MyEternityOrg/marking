from django.shortcuts import render
from django.views.generic import FormView, DetailView, ListView
from django.views.generic.edit import BaseFormView

from Marking.mixin import *
from .models import *


class IndexPageFormView(BaseClassContextMixin, ListView):
    title = 'Система маркировки'
    template_name = 'Main/index.html'
    model = ModelDocuments
    paginate_by = 50