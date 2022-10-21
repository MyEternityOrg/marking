from django import forms
from django.forms import formset_factory
from django.forms import Form
from .models import *


class FormDocuments(forms.ModelForm):
    guid = forms.CharField()

    class Meta:
        model = ModelDocuments
        fields = '__all__'
        # exclude = ('dts',)


class FormContractor(forms.ModelForm):
    contractor_guid = forms.CharField(max_length=64, required=False, disabled=True)
    contractor_name = forms.CharField(max_length=128)
    contractor_inn = forms.CharField(max_length=128, disabled=True, required=False)
    distributor = forms.BooleanField(required=False)
    contractor_count_whitelist = forms.BooleanField(required=False)
    contractor_quality_whitelist = forms.BooleanField(required=False)
    contractor_mrc_minimal = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        super(FormContractor, self).__init__(*args, **kwargs)

        self.fields['contractor_guid'].widget.attrs['class'] = 'form-control'
        self.fields['contractor_guid'].widget.attrs['name'] = 'contractor_guid'

        self.fields['contractor_name'].widget.attrs['class'] = 'form-control'

        self.fields['contractor_inn'].widget.attrs['class'] = 'form-control'
        self.fields['contractor_inn'].widget.attrs['name'] = 'contractor_inn'

        self.fields['distributor'].widget.attrs['class'] = 'form-check-input'
        self.fields['distributor'].widget.attrs['type'] = 'checkbox'

        self.fields['contractor_count_whitelist'].widget.attrs['class'] = 'form-check-input'
        self.fields['contractor_count_whitelist'].widget.attrs['type'] = 'checkbox'

        self.fields['contractor_quality_whitelist'].widget.attrs['class'] = 'form-check-input'
        self.fields['contractor_quality_whitelist'].widget.attrs['type'] = 'checkbox'

        self.fields['contractor_mrc_minimal'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelContractors
        fields = '__all__'
