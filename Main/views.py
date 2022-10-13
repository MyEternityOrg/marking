from django.shortcuts import render
from django.views.generic import FormView, DetailView, ListView
from django.views.generic.edit import BaseFormView

from Marking.mixin import *
from .models import *

# Create your views here.


class IndexPageFormView(BaseClassContextMixin, ListView):
    title = 'Главная страница'
    template_name = 'Main/index.html'
    model = ModelDocuments
