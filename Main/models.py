import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ModelCheckStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True, editable=False, auto_created=True, verbose_name='ID статуса')
    status_name = models.CharField(max_length=128, verbose_name='Статус проверки')
    finished = models.IntegerField(default=0, verbose_name='Конечный статус')

    class Meta:
        db_table = 'check_statuses'
        managed = False


class ModelDocumentStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True, editable=False, auto_created=True, verbose_name='ID статуса')
    status_description = models.CharField(max_length=512, verbose_name='Статус документа')
    status_level = models.IntegerField(default=-1, verbose_name='Уровень статуса')

    class Meta:
        db_table = 'document_statuses'
        managed = False


class ModelErpStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True, editable=False, auto_created=True, verbose_name='ID статуса')
    status_description = models.CharField(max_length=512, verbose_name='Статус ERP')

    class Meta:
        db_table = 'erp_statuses'
        managed = False


class ModelMarkTypes(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, auto_created=True, verbose_name='ID Вида Маркировки')
    description = models.CharField(max_length=512, verbose_name='Описание вида маркировки')
    hs_flag = models.CharField(max_length=64, verbose_name='Вид для ВМС')
    ts_group_code = models.IntegerField(default=0, verbose_name='ID Системы "Честный знак"')

    class Meta:
        db_table = 'mark_types'
        managed = False


class ModelContractors(models.Model):
    guid = models.CharField(primary_key=True, editable=False, default=uuid.uuid4(), max_length=64,
                            verbose_name='GUID Контрагента')
    contractor_name = models.CharField(max_length=150, verbose_name='Наименование')
    contractor_inn = models.CharField(max_length=32, verbose_name='ИНН')
    contractor_count_whitelist = models.IntegerField(default=0, verbose_name='Белый список по количеству')
    contractor_quality_whitelist = models.IntegerField(default=0, verbose_name='Белый список по качеству')
    contractor_mrc_minimal = models.IntegerField(default=0, verbose_name='Контролировать минимальную МРЦ')

    class Meta:
        db_table = 'contractors'
        managed = False


class ModelContractorContacts(models.Model):
    contractor_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE, verbose_name='GUID Контакта')
    email = models.CharField(primary_key=True, unique=True, max_length=128, verbose_name='Электронная почта')
    name = models.CharField(max_length=512, verbose_name='Наименование')

    class Meta:
        db_table = 'contractor_contacts'
        managed = False


class ModelDocuments(models.Model):
    guid = models.CharField(primary_key=True, editable=False, default=uuid.uuid4(), max_length=64,
                            verbose_name='GUID Документа')
    contractor_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE, verbose_name='Контрагент')
    order_guid = models.CharField(max_length=64, default=uuid.uuid4(), verbose_name='Заказ')
    income_guid = models.CharField(max_length=64, default=uuid.uuid4(), verbose_name='Приход')
    document_date = models.DateField(verbose_name='Дата документа')
    document_number = models.CharField(max_length=128, verbose_name='Номер документа')
    document_name = models.CharField(max_length=512, verbose_name='Наименование документа')
    document_id = models.CharField(max_length=128, verbose_name='Идентификатор ЭДО')
    check_status_id = models.ForeignKey(ModelCheckStatuses, on_delete=models.DO_NOTHING,
                                        verbose_name='Статус проверки ЧЗ')
    whitelisted = models.IntegerField(editable=False, verbose_name='Документ в белом списке')
    document_status_id = models.ForeignKey(ModelDocumentStatuses, on_delete=models.DO_NOTHING,
                                           verbose_name='Статус проверки СМ')
    erp_status_id = models.ForeignKey(ModelErpStatuses, on_delete=models.DO_NOTHING,
                                      verbose_name='Статус в ERP системе')
    allowed_gray_zone = models.IntegerField(default=0, editable=False, verbose_name='Разрешена серая зона')

    class Meta:
        db_table = 'documents'
        managed = False
