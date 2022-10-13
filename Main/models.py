import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ModelCisStatuses(models.Model):
    status_name = models.CharField(primary_key=True, max_length=128, verbose_name='Статус ЧЗ')
    status_local_name = models.CharField(max_length=128, verbose_name='Описание статуса')
    status_correct = models.IntegerField(default=0, verbose_name='Разрешена приемка')
    valid_to = models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Действителен ДО')

    class Meta:
        db_table = 'cis_statuses'
        managed = False


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
    hs_flag = models.CharField(max_length=64, verbose_name='Вид продукции ВМС')
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


class ModelOrders(models.Model):
    guid = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=64, editable=False,
                            verbose_name='GUID Заказа')
    order_status = models.BooleanField(default=True, verbose_name='Заказ завершен')
    order_number = models.CharField(max_length=150, verbose_name='Номер заказа')
    delivery_date = models.DateField(auto_now_add=False, default=datetime.date(2000, 1, 1), verbose_name='Дата заказа')
    contractor_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE, verbose_name='Контрагент')

    class Meta:
        db_table = 'orders'
        managed = False


class ModelIncomes(models.Model):
    guid = models.CharField(editable=False, primary_key=True, max_length=64, default=uuid.uuid4(),
                            verbose_name='GUID Прихода')
    internal_document_number = models.CharField(editable=False, max_length=128,
                                                verbose_name='Внутренний номер документа')
    external_document_number = models.CharField(editable=False, max_length=128,
                                                verbose_name='Номер документа контрагента')
    document_date = models.DateField(editable=False, default=datetime.date(2000, 1, 1), verbose_name='Дата документа')
    document_fobj = models.CharField(editable=False, max_length=64, verbose_name='Указатель')
    erp_status_id = models.ForeignKey(ModelErpStatuses, on_delete=models.DO_NOTHING, verbose_name='Статус документа')

    class Meta:
        db_table = 'incomes'
        managed = False


class ModelIncomeData(models.Model):
    document_guid = models.ForeignKey(ModelIncomes, on_delete=models.CASCADE, verbose_name='Приходная накладная')
    internal_ware_code = models.CharField(db_column='internal_warecode', editable=False, max_length=256,
                                          verbose_name='Артикул товара')
    contractor_ware_count = models.FloatField(db_column='internal_warecount', editable=False, default=0,
                                              verbose_name='Количество')
    contractor_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Контрагента')

    class Meta:
        db_table = 'income_data'
        managed = False


class ModelDocuments(models.Model):
    guid = models.CharField(primary_key=True, editable=False, default=uuid.uuid4(), max_length=64,
                            verbose_name='GUID Документа')
    contractor_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE, verbose_name='Контрагент')
    order_guid = models.ForeignKey(ModelOrders, on_delete=models.DO_NOTHING, verbose_name='Заказ')
    income_guid = models.ForeignKey(ModelIncomes, on_delete=models.DO_NOTHING, verbose_name='Приход')
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


class ModelWares(models.Model):
    ware_guid = models.CharField(editable=False, default=uuid.uuid4(), max_length=64, verbose_name='GUID Продукции')
    ware_code = models.CharField(editable=False, max_length=32, verbose_name='Артикул продукции')
    ware_name = models.CharField(editable=False, max_length=150, verbose_name='Наименование продукции')
    ware_data = models.CharField(editable=False, max_length=128, verbose_name='Данные ШК/Кода продукции')
    marked = models.BooleanField(editable=False, default=0, verbose_name='Пометка удаления')
    lvl1_qty = models.FloatField(editable=False, default=0, verbose_name='Коэффициент упаковки')

    class Meta:
        db_table = 'wares'
        managed = False


class ModelWaresGtins(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4(), verbose_name='GUID Записи')
    ware_guid = models.ForeignKey(ModelWares, on_delete=models.DO_NOTHING, verbose_name='Продукция')
    ware_gtin = models.CharField(editable=False, max_length=64, verbose_name='GTIN Продукции')
    ts_group_code = models.IntegerField(editable=False, verbose_name='ID Вида Маркировки')

    class Meta:
        db_table = 'wares_gtins'
        managed = False


class ModelWaresMarks(models.Model):
    ware_guid = models.ForeignKey(ModelWares, on_delete=models.DO_NOTHING, verbose_name='Продукция')
    period = models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата начала действия')
    hs_flag = models.CharField(default='HS:NONE', max_length=64, null=False, verbose_name='Вид продукции ВМС')

    class Meta:
        db_table = 'wares_marks'
        managed = False


class ModelDocumentContractorCis(models.Model):
    document_guid = models.ForeignKey(ModelDocuments, on_delete=models.CASCADE, verbose_name='Документ')
    internal_ware_code = models.ForeignKey(ModelWares, db_column='contractor_warecode', on_delete=models.DO_NOTHING,
                                           verbose_name='Продукция'),
    contractor_ware_code = models.CharField(db_column='contractor_warecode', editable=False, max_length=128,
                                            verbose_name='ЛК Контрагента')
    contractor_barcode = models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')
    contractor_ware_count = models.FloatField(editable=False, db_column='contractor_warecount', default=0,
                                              verbose_name='Количество')
    contractor_cis = models.CharField(max_length=256, editable=False, verbose_name='КИЗ/КИТУ')

    class Meta:
        db_table = 'document_contractor_cis'
        managed = False


class ModelDocumentDetailedCis(models.Model):
    document_guid = models.ForeignKey(ModelDocuments, on_delete=models.CASCADE, verbose_name='Документ')
    owner_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE, verbose_name='Контрагент')
    contractor_ware_code = models.CharField(db_column='contractor_warecode', editable=False, max_length=128,
                                            verbose_name='ЛК Контрагента')
    contractor_barcode = models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')
    unit_parent_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Агрегата')
    unit_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ')
    unit_produced_date = models.DateField(editable=False, default=datetime.date(2000, 1, 1),
                                          verbose_name='Дата производства')
    unit_package_type = models.CharField(editable=False, max_length=64, verbose_name='Вид упаковки')
    unit_status_id = models.ForeignKey(ModelCisStatuses, on_delete=models.DO_NOTHING, verbose_name='Статус ЧЗ')
    unit_childs = models.FloatField(editable=False, default=0, verbose_name='Дочерних КИЗ/КИТУ')
    unit_check_error_code = models.CharField(editable=False, max_length=64, default='', verbose_name='Код ошибки ЧЗ')
    unit_check_error_message = models.CharField(editable=False, max_length=256, verbose_name='Описание ошибки ЧЗ')
    mrc_value = models.IntegerField(editable=False, default=0, verbose_name='Значение МРЦ')

    class Meta:
        db_table = 'document_detailed_cis'
        managed = False


class ModelDocumentGrayZone(models.Model):
    document_guid = models.ForeignKey(ModelDocuments, on_delete=models.CASCADE, verbose_name='Документ')
    unit_package_type = models.CharField(editable=False, max_length=64, verbose_name='Вид упаковки')
    unit_parent_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Агрегата')
    unit_cis = models.CharField(editable=False, max_length=256, verbose_name='Виртуальный КИЗ/КИТУ')
    unit_cis_original = models.CharField(editable=False, max_length=256, verbose_name='Исходный КИЗ/КИТУ')
    contractor_ware_code = models.CharField(db_column='contractor_warecode', editable=False, max_length=128,
                                            verbose_name='ЛК Контрагента')
    contractor_barcode = models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')

    class Meta:
        db_table = 'document_grayzone'
        managed = False


class ModelDocumentCheckResult(models.Model):
    document_guid = models.ForeignKey(ModelDocuments, on_delete=models.CASCADE, verbose_name='Документ')
    ware_code = models.CharField(editable=False, max_length=32, verbose_name='Артикул продукции')
    ware_name = models.CharField(editable=False, max_length=256, verbose_name='Наименование продукции')
    contractor_cis = models.CharField(max_length=256, editable=False, verbose_name='КИЗ/КИТУ')
    gtin = models.CharField(max_length=64, editable=False, verbose_name='GTIN')
    reason = models.CharField(max_length=512, editable=False, verbose_name='Описание ошибки')

    class Meta:
        db_table = 'document_check_result'
        managed = False
