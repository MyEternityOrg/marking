import datetime

import django_filters
from django.forms import DateInput
from django_filters import *
from django_filters.fields import DateRangeField
from django_filters.widgets import RangeWidget, DateRangeWidget

from .models import *


class FilterWares(django_filters.FilterSet):
    ware_code = CharFilter(lookup_expr='contains', label='Код товара')
    ware_name = CharFilter(lookup_expr='contains', label='Наименование товара')

    def __init__(self, *args, **kwargs):
        super(FilterWares, self).__init__(*args, **kwargs)
        self.form.fields['ware_code'].widget.attrs['id'] = 'ware_code_id'
        self.form.fields['ware_code'].widget.attrs['class'] = 'form-control'
        self.form.fields['ware_code'].widget.attrs['style'] = 'width: 150px'
        self.form.fields['ware_code'].widget.attrs['placeholder'] = 'ЛК'
        self.form.fields['ware_name'].widget.attrs['id'] = 'ware_code_id'
        self.form.fields['ware_name'].widget.attrs['class'] = 'form-control'
        self.form.fields['ware_name'].widget.attrs['style'] = 'width: 250px'
        self.form.fields['ware_name'].widget.attrs['placeholder'] = 'Наименование'

    class Meta:
        model = ModelWares
        fields = {'ware_code', 'ware_name'}


class FilterDocumentsList(django_filters.FilterSet):
    document_date = DateFromToRangeFilter(label='Период:',
                                          widget=DateRangeWidget(attrs={'type': 'date', 'input_type': 'date'}))
    contractor_guid = ModelChoiceFilter(queryset=ModelContractors.objects.all().order_by('contractor_name'),
                                        label='Контрагент', empty_label='---Контрагент---')

    def __init__(self, *args, **kwargs):
        super(FilterDocumentsList, self).__init__(*args, **kwargs)
        self.form.fields['contractor_guid'].widget.attrs['id'] = 'contractor_guid'
        self.form.fields['contractor_guid'].widget.attrs['class'] = 'form-select'
        self.form.fields['contractor_guid'].widget.attrs['style'] = 'width: 40%'
        self.form.fields['contractor_guid'].widget.attrs['selected'] = 'Контрагент'
        self.form.fields['document_date'].widget.attrs['id'] = 'date_range'
        self.form.fields['document_date'].widget.attrs['class'] = 'form-control'
        self.form.fields['document_date'].widget.attrs['style'] = 'width: 5px'

    class Meta:
        model = ModelDocuments
        fields = {'contractor_guid', 'document_date'}
