from django import forms
from django.forms import formset_factory
from django.forms import Form
from .models import ModelDocuments


class FormDocuments(forms.ModelForm):
    guid = forms.CharField()

    class Meta:
        model = ModelDocuments
        fields = '__all__'
        # exclude = ('dts',)


