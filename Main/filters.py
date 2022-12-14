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
    marked = BooleanFilter(label='Пометка удаления')

    def __init__(self, *args, **kwargs):
        super(FilterWares, self).__init__(*args, **kwargs)
        self.form.fields['ware_code'].widget.attrs['id'] = 'ware_code_id'
        self.form.fields['ware_code'].widget.attrs['class'] = 'form-control'
        self.form.fields['ware_code'].widget.attrs['style'] = 'margin-right: 10px; min-width: 150px;'
        self.form.fields['ware_code'].widget.attrs['placeholder'] = 'ЛК'
        self.form.fields['ware_name'].widget.attrs['id'] = 'ware_name_id'
        self.form.fields['ware_name'].widget.attrs['class'] = 'form-control'
        self.form.fields['ware_name'].widget.attrs['style'] = 'margin-left: 10px; min-width: 300px;'
        self.form.fields['ware_name'].widget.attrs['placeholder'] = 'Наименование'
        self.form.fields['marked'].widget.attrs['class'] = 'form-select'
        self.form.fields['marked'].widget.attrs['style'] = 'margin-left: 10px; min-width: 100px;'

    class Meta:
        model = ModelWares
        fields = {'ware_code', 'ware_name', 'marked'}


class FilterDocumentsList(django_filters.FilterSet):
    document_date = DateFromToRangeFilter(label='Период:',
                                          widget=DateRangeWidget(attrs={'type': 'date', 'input_type': 'date'}))
    contractor_guid = ModelChoiceFilter(queryset=ModelContractors.objects.filter(distributor=True),
                                        label='Контрагент', empty_label='---Контрагент---')
    document_status_id = ModelChoiceFilter(queryset=ModelDocumentStatuses.objects.all().order_by('status_id'),
                                           label='Статус', empty_label='---Статус---')
    document_id = CharFilter(lookup_expr='contains', label='ИД документа')

    def __init__(self, *args, **kwargs):
        super(FilterDocumentsList, self).__init__(*args, **kwargs)
        self.form.fields['contractor_guid'].widget.attrs['id'] = 'contractor_guid'
        self.form.fields['contractor_guid'].widget.attrs['class'] = 'form-select'
        self.form.fields['contractor_guid'].widget.attrs['style'] = 'min-width: 300px;'
        self.form.fields['contractor_guid'].widget.attrs['selected'] = 'Контрагент'
        self.form.fields['contractor_guid'].widget.attrs['style'] = 'margin-left: 10px; margin-right: 10px;'
        self.form.fields['document_status_id'].widget.attrs['id'] = 'document_status_id'
        self.form.fields['document_status_id'].widget.attrs['class'] = 'form-select'
        self.form.fields['document_status_id'].widget.attrs[
            'style'] = 'margin-right: 10px; min-width: 150px; max-width: 400px'
        self.form.fields['document_status_id'].widget.attrs['selected'] = 'Статус'
        self.form.fields['document_date'].widget.attrs['id'] = 'date_range'
        self.form.fields['document_date'].widget.attrs['class'] = 'form-control'
        self.form.fields['document_date'].widget.attrs['style'] = 'min-width: 150px; max-width: 150px;'
        self.form.fields['document_id'].widget.attrs['id'] = 'document_id'
        self.form.fields['document_id'].widget.attrs['class'] = 'form-control'
        self.form.fields['document_id'].widget.attrs['style'] = 'margin-right: 10px; min-width: 200px; max-width: 200px'
        self.form.fields['document_id'].widget.attrs['placeholder'] = 'ИД документа'

    class Meta:
        model = ModelDocuments
        fields = {'contractor_guid', 'document_date', 'document_status_id', 'document_id'}
