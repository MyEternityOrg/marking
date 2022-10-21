import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Count


class ModelCisStatuses(models.Model):
    """
        Статусы КИЗ/КИТУ

        status_name - Наименование статуса в системе ЧЗ

        status_local_name - Локализованное наименование статуса.

        status_correct - Считать статус корректным при проверках.

        valid_to - Статус считается корректным пока действует до указанной даты.
    """
    status_name = models.CharField(null=False, primary_key=True, default='EMPTY', max_length=128,
                                   verbose_name='Статус ЧЗ')
    status_local_name = models.CharField(null=False, default='Пустой', max_length=128, verbose_name='Описание статуса')
    status_correct = models.IntegerField(null=False, default=0, verbose_name='Разрешена приемка')
    valid_to = models.DateField(null=False, default=datetime.date(2000, 1, 1), verbose_name='Действителен ДО')

    class Meta:
        db_table = 'cis_statuses'
        managed = False


class ModelCheckStatuses(models.Model):
    status_id = models.IntegerField(null=False, primary_key=True, editable=False, auto_created=True,
                                    verbose_name='ID статуса')
    status_name = models.CharField(null=False, default='Неизвестно', max_length=128, verbose_name='Статус проверки')
    finished = models.IntegerField(null=False, default=0, verbose_name='Конечный статус')

    class Meta:
        db_table = 'check_statuses'
        managed = False


class ModelDocumentStatuses(models.Model):
    """
        Статусы проверки документов системой.

        status_id - Код статуса

        status_description - Описание статуса

        status_level - Уровень ошибки статуса (0 - статyс корректен)
    """
    status_id = models.IntegerField(null=False, primary_key=True, editable=False, auto_created=True,
                                    verbose_name='ID статуса')
    status_description = models.CharField(null=False, default='Нет описания', max_length=512,
                                          verbose_name='Статус документа')
    status_level = models.IntegerField(null=False, default=-1, verbose_name='Уровень статуса')

    def __str__(self):
        return f'{self.status_description} [{self.status_id}]'

    class Meta:
        db_table = 'document_statuses'
        managed = False


class ModelErpStatuses(models.Model):
    status_id = models.IntegerField(null=False, primary_key=True, editable=False, auto_created=True,
                                    verbose_name='ID статуса')
    status_description = models.CharField(null=False, default='Нет описания', max_length=512, verbose_name='Статус ERP')

    class Meta:
        db_table = 'erp_statuses'
        managed = False


class ModelMarkTypes(models.Model):
    id = models.IntegerField(null=False, primary_key=True, editable=False, auto_created=True,
                             verbose_name='ID Вида Маркировки')
    description = models.CharField(null=False, default='Нет описания вида', max_length=512,
                                   verbose_name='Описание вида маркировки')
    hs_flag = models.CharField(null=False, default='HS:NONE', max_length=64, verbose_name='Вид продукции ВМС')
    ts_group_code = models.IntegerField(null=False, default=-1, verbose_name='ID Системы "Честный знак"')

    class Meta:
        db_table = 'mark_types'
        managed = False


class ModelContractors(models.Model):
    """
        Контрагенты

        contractor_guid - Идентификатор контрагента.

        contractor_name - Наименование контрагента.

        contractor_inn - ИНН

        contractor_count_whitelist - Контрагент не проходит проверку количества.

        contractor_quantity_whitelist - Контрагент не проходит проверку качества.

        contractor_mrc_minimal - Минимальная цена товара контрагента.
    """
    contractor_guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4(),
                                       max_length=64,
                                       verbose_name='GUID Контрагента')
    distributor = models.BooleanField(default=False, verbose_name='Поставщик')
    contractor_name = models.CharField(max_length=150, verbose_name='Наименование')
    contractor_inn = models.CharField(max_length=32, verbose_name='ИНН')
    contractor_count_whitelist = models.BooleanField(default=False, verbose_name='Белый список по количеству')
    contractor_quality_whitelist = models.BooleanField(default=False, verbose_name='Белый список по качеству')
    contractor_mrc_minimal = models.IntegerField(default=0, verbose_name='Контролировать минимальную МРЦ')

    def __str__(self):
        return f'{self.contractor_name} [{self.contractor_inn}]'


    class Meta:
        db_table = 'contractors'
        ordering = ('contractor_name',)
        managed = False


class ModelContractorContacts(models.Model):
    contractor_guid = models.ForeignKey(ModelContractors, db_column='contractor_guid', on_delete=models.CASCADE,
                                        verbose_name='GUID Контакта')
    email = models.CharField(primary_key=True, unique=True, max_length=128, verbose_name='Электронная почта')
    name = models.CharField(max_length=512, verbose_name='Наименование')

    class Meta:
        db_table = 'contractor_contacts'
        managed = False


class ModelOrders(models.Model):
    guid = models.CharField(db_column='guid', primary_key=True, default=uuid.uuid4(), max_length=64, editable=False,
                            verbose_name='GUID Заказа')
    order_status = models.BooleanField(default=True, verbose_name='Заказ завершен')
    order_number = models.CharField(max_length=150, verbose_name='Номер заказа')
    delivery_date = models.DateField(auto_now_add=False, default=datetime.date(2000, 1, 1), verbose_name='Дата заказа')
    contractor_guid = models.ForeignKey(ModelContractors, db_column='contractor_guid', on_delete=models.CASCADE,
                                        verbose_name='Контрагент')

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
    erp_status_id = models.ForeignKey(ModelErpStatuses, db_column='erp_status_id', on_delete=models.DO_NOTHING,
                                      verbose_name='Статус документа')

    class Meta:
        db_table = 'incomes'
        managed = False


class ModelIncomeData(models.Model):
    document_guid = models.ForeignKey(ModelIncomes, db_column='document_guid', on_delete=models.CASCADE,
                                      verbose_name='Приходная накладная')
    internal_ware_code = models.CharField(db_column='internal_warecode', editable=False, max_length=256,
                                          verbose_name='Артикул товара')
    contractor_ware_count = models.FloatField(db_column='internal_warecount', editable=False, default=0,
                                              verbose_name='Количество')
    contractor_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Контрагента')

    class Meta:
        db_table = 'income_data'
        managed = False


class ModelDocuments(models.Model):
    """
        Документы УПД с маркированной продукцией (модель).

        guid: Идентификатор системы маркировки

        contractor_guid: Контрагент

        order_guid - Заказ

        income_guid - Приход

        document_date - Дата документа

        document_number - Номер документа

        document_id - Идентификатор документа в ЭДО

        check_status_id - Результат проверки в системе Честный знак

        document_status_id - Результат сверки состава документа системой маркировки.

        erp_status_id - Состояние документа УПД в ERP системе.

        whitelisted - Документ помечен как "исключение" из проверки качества/количества (document_status)

        allowed_gray_zone - Документ разрешен к приемке с серой зоной.

    """

    guid = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=64,
                            verbose_name='GUID Документа')
    contractor_guid = models.ForeignKey(ModelContractors, db_column='contractor_guid', on_delete=models.CASCADE,
                                        verbose_name='Контрагент')
    order_guid = models.ForeignKey(ModelOrders, db_column='order_guid', on_delete=models.DO_NOTHING,
                                   verbose_name='Заказ')
    income_guid = models.ForeignKey(ModelIncomes, db_column='income_guid', on_delete=models.DO_NOTHING,
                                    verbose_name='Приход')
    document_date = models.DateField(verbose_name='Дата документа', db_column='document_date', null=False,
                                     default=datetime.date(2000, 1, 1))
    document_number = models.CharField(max_length=128, verbose_name='Номер документа')
    document_name = models.CharField(max_length=512, verbose_name='Наименование документа')
    document_id = models.CharField(max_length=128, verbose_name='Идентификатор ЭДО')
    check_status_id = models.ForeignKey(ModelCheckStatuses, db_column='check_status_id', on_delete=models.DO_NOTHING,
                                        verbose_name='Статус проверки ЧЗ')
    whitelisted = models.IntegerField(verbose_name='Документ в белом списке')
    document_status_id = models.ForeignKey(ModelDocumentStatuses, db_column='document_status_id',
                                           on_delete=models.DO_NOTHING,
                                           verbose_name='Статус проверки СМ')
    erp_status_id = models.ForeignKey(ModelErpStatuses, db_column='erp_status_id', on_delete=models.DO_NOTHING,
                                      verbose_name='Статус в ERP системе')
    allowed_gray_zone = models.IntegerField(default=0, db_column='allowed_grayzone',
                                            verbose_name='Разрешена серая зона')


    class Meta:
        db_table = 'documents'
        managed = False
        ordering = ('-document_date', 'contractor_guid', 'document_number')


class ModelWares(models.Model):
    """
        Справочник номенклатуры

        ware_guid - Идентификатор товаро

        ware_code - Код товара.

        ware_name - Наименование товара

        ware_data - Штрих код товара.

        marked - Признак удаления товара.

        lvl1_qty - Коэффициент/множитель родительской упаковки
    """
    ware_guid = models.CharField(primary_key=True, db_column='ware_guid', default=uuid.uuid4(), max_length=64,
                                 verbose_name='GUID Продукции')
    ware_code = models.CharField(max_length=32, verbose_name='Артикул продукции')
    ware_name = models.CharField(max_length=150, verbose_name='Наименование продукции')
    ware_data = models.CharField(max_length=128, verbose_name='Данные ШК/Кода продукции')
    marked = models.BooleanField(default=0, verbose_name='Пометка удаления')
    lvl1_qty = models.FloatField(default=0, verbose_name='Коэффициент упаковки')

    @classmethod
    def get_records(cls):
        return cls.objects.values(''
                                  'ware_guid',
                                  'ware_code',
                                  'ware_name',
                                  'marked'). \
            annotate(ware_data=Max('ware_data'), lvl1_qty=Max('lvl1_qty')). \
            order_by('ware_code')

    class Meta:
        db_table = 'wares'
        managed = False
        constraints = [
            models.UniqueConstraint(fields=['ware_guid', 'ware_data'], name="%(app_label)s_%(class)s_unique"),
        ]


class ModelWaresGtins(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4(), verbose_name='GUID Записи')
    ware_guid = models.ForeignKey(ModelWares, db_column='ware_guid', on_delete=models.DO_NOTHING,
                                  verbose_name='Продукция')
    ware_gtin = models.CharField(editable=False, max_length=64, verbose_name='GTIN Продукции')
    ts_group_code = models.IntegerField(editable=False, verbose_name='ID Вида Маркировки')

    class Meta:
        db_table = 'wares_gtins'
        managed = False


class ModelWaresMarks(models.Model):
    ware_guid = models.ForeignKey(ModelWares, db_column='ware_guid', on_delete=models.DO_NOTHING,
                                  verbose_name='Продукция')
    period = models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата начала действия')
    hs_flag = models.CharField(default='HS:NONE', max_length=64, null=False, verbose_name='Вид продукции ВМС')

    class Meta:
        db_table = 'wares_marks'
        managed = False


class ModelDocumentContractorCis(models.Model):
    document_guid = models.ForeignKey(ModelDocuments, db_column='document_guid', on_delete=models.CASCADE,
                                      verbose_name='Документ')
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
    document_guid = models.ForeignKey(ModelDocuments, db_column='document_guid', on_delete=models.CASCADE,
                                      verbose_name='Документ')
    owner_guid = models.ForeignKey(ModelContractors, db_column='owner_guid', on_delete=models.CASCADE,
                                   verbose_name='Контрагент')
    contractor_ware_code = models.CharField(db_column='contractor_warecode', editable=False, max_length=128,
                                            verbose_name='ЛК Контрагента')
    contractor_barcode = models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')
    unit_parent_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Агрегата')
    unit_cis = models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ')
    unit_produced_date = models.DateField(editable=False, default=datetime.date(2000, 1, 1),
                                          verbose_name='Дата производства')
    unit_package_type = models.CharField(editable=False, max_length=64, verbose_name='Вид упаковки')
    unit_status_id = models.ForeignKey(ModelCisStatuses, db_column='unit_status_id', on_delete=models.DO_NOTHING,
                                       verbose_name='Статус ЧЗ')
    unit_childs = models.FloatField(editable=False, default=0, verbose_name='Дочерних КИЗ/КИТУ')
    unit_check_error_code = models.CharField(editable=False, max_length=64, default='', verbose_name='Код ошибки ЧЗ')
    unit_check_error_message = models.CharField(editable=False, max_length=256, verbose_name='Описание ошибки ЧЗ')
    mrc_value = models.IntegerField(editable=False, default=0, verbose_name='Значение МРЦ')

    class Meta:
        db_table = 'document_detailed_cis'
        managed = False


class ModelDocumentGrayZone(models.Model):
    document_guid = models.ForeignKey(ModelDocuments, db_column='document_id', on_delete=models.CASCADE,
                                      verbose_name='Документ')
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
    document_guid = models.ForeignKey(ModelDocuments, db_column='document_guid', on_delete=models.CASCADE,
                                      verbose_name='Документ')
    ware_code = models.CharField(editable=False, max_length=32, verbose_name='Артикул продукции')
    ware_name = models.CharField(editable=False, max_length=256, verbose_name='Наименование продукции')
    contractor_cis = models.CharField(max_length=256, editable=False, verbose_name='КИЗ/КИТУ')
    gtin = models.CharField(max_length=64, editable=False, verbose_name='GTIN')
    reason = models.CharField(max_length=512, editable=False, verbose_name='Описание ошибки')

    class Meta:
        db_table = 'document_check_result'
        managed = False
