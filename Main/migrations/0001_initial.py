# Generated by Django 4.0.8 on 2022-11-09 17:06

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelCheckStatuses',
            fields=[
                ('status_id', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID статуса')),
                ('status_name', models.CharField(default='Неизвестно', max_length=128, verbose_name='Статус проверки')),
                ('finished', models.IntegerField(default=0, verbose_name='Конечный статус')),
            ],
            options={
                'db_table': 'check_statuses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelCisStatuses',
            fields=[
                ('status_name', models.CharField(default='EMPTY', max_length=128, primary_key=True, serialize=False, verbose_name='Статус ЧЗ')),
                ('status_local_name', models.CharField(default='Пустой', max_length=128, verbose_name='Описание статуса')),
                ('status_correct', models.IntegerField(default=0, verbose_name='Разрешена приемка')),
                ('valid_to', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Действителен ДО')),
            ],
            options={
                'verbose_name': 'Статус КИ/КИЗ',
                'verbose_name_plural': 'Статусы КИ/КИЗ',
                'db_table': 'cis_statuses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelContractorContacts',
            fields=[
                ('email', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True, verbose_name='Электронная почта')),
                ('name', models.CharField(max_length=512, verbose_name='Наименование')),
            ],
            options={
                'db_table': 'contractor_contacts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelContractors',
            fields=[
                ('contractor_guid', models.CharField(db_column='guid', default=uuid.UUID('50650738-a25b-4623-857a-c025fd1caeb7'), max_length=64, primary_key=True, serialize=False, verbose_name='GUID Контрагента')),
                ('distributor', models.BooleanField(default=False, verbose_name='Поставщик')),
                ('contractor_name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('contractor_inn', models.CharField(max_length=32, verbose_name='ИНН')),
                ('contractor_count_whitelist', models.BooleanField(default=False, verbose_name='Белый список по количеству')),
                ('contractor_quality_whitelist', models.BooleanField(default=False, verbose_name='Белый список по качеству')),
                ('contractor_mrc_minimal', models.IntegerField(default=0, verbose_name='Контролировать минимальную МРЦ')),
            ],
            options={
                'db_table': 'contractors',
                'ordering': ('contractor_name',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelDocumentCheckResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ware_code', models.CharField(editable=False, max_length=32, verbose_name='Артикул продукции')),
                ('ware_name', models.CharField(editable=False, max_length=256, verbose_name='Наименование продукции')),
                ('contractor_cis', models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ')),
                ('gtin', models.CharField(editable=False, max_length=64, verbose_name='GTIN')),
                ('reason', models.CharField(editable=False, max_length=512, verbose_name='Описание ошибки')),
            ],
            options={
                'db_table': 'document_check_result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelDocumentContractorCis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractor_ware_code', models.CharField(db_column='contractor_warecode', editable=False, max_length=128, verbose_name='ЛК Контрагента')),
                ('contractor_barcode', models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')),
                ('contractor_ware_count', models.FloatField(db_column='contractor_warecount', default=0, editable=False, verbose_name='Количество')),
                ('contractor_cis', models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ')),
            ],
            options={
                'db_table': 'document_contractor_cis',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelDocumentDetailedCis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractor_ware_code', models.CharField(db_column='contractor_warecode', editable=False, max_length=128, verbose_name='ЛК Контрагента')),
                ('contractor_barcode', models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')),
                ('unit_parent_cis', models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Агрегата')),
                ('unit_cis', models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ')),
                ('unit_produced_date', models.DateField(default=datetime.date(2000, 1, 1), editable=False, verbose_name='Дата производства')),
                ('unit_package_type', models.CharField(editable=False, max_length=64, verbose_name='Вид упаковки')),
                ('unit_childs', models.FloatField(default=0, editable=False, verbose_name='Дочерних КИЗ/КИТУ')),
                ('unit_check_error_code', models.CharField(default='', editable=False, max_length=64, verbose_name='Код ошибки ЧЗ')),
                ('unit_check_error_message', models.CharField(editable=False, max_length=256, verbose_name='Описание ошибки ЧЗ')),
                ('mrc_value', models.IntegerField(default=0, editable=False, verbose_name='Значение МРЦ')),
            ],
            options={
                'db_table': 'document_detailed_cis',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelDocumentGrayZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_package_type', models.CharField(editable=False, max_length=64, verbose_name='Вид упаковки')),
                ('unit_parent_cis', models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Агрегата')),
                ('unit_cis', models.CharField(editable=False, max_length=256, verbose_name='Виртуальный КИЗ/КИТУ')),
                ('unit_cis_original', models.CharField(editable=False, max_length=256, verbose_name='Исходный КИЗ/КИТУ')),
                ('contractor_ware_code', models.CharField(db_column='contractor_warecode', editable=False, max_length=128, verbose_name='ЛК Контрагента')),
                ('contractor_barcode', models.CharField(editable=False, max_length=128, verbose_name='ШК Контрагента')),
            ],
            options={
                'db_table': 'document_grayzone',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelDocuments',
            fields=[
                ('guid', models.CharField(default=uuid.UUID('a353bd0e-d1d7-4de6-ab03-b72f7ec2a866'), max_length=64, primary_key=True, serialize=False, verbose_name='GUID Документа')),
                ('document_date', models.DateField(db_column='document_date', default=datetime.date(2000, 1, 1), verbose_name='Дата документа')),
                ('document_number', models.CharField(max_length=128, verbose_name='Номер документа')),
                ('document_name', models.CharField(max_length=512, verbose_name='Наименование документа')),
                ('document_id', models.CharField(max_length=128, verbose_name='Идентификатор ЭДО')),
                ('whitelisted', models.IntegerField(verbose_name='Документ в белом списке')),
                ('allowed_gray_zone', models.IntegerField(db_column='allowed_grayzone', default=0, verbose_name='Разрешена серая зона')),
            ],
            options={
                'db_table': 'documents',
                'ordering': ('-document_date', 'contractor_guid', 'document_number'),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelDocumentStatuses',
            fields=[
                ('status_id', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID статуса')),
                ('status_description', models.CharField(default='Нет описания', max_length=512, verbose_name='Статус документа')),
                ('status_level', models.IntegerField(default=-1, verbose_name='Уровень статуса')),
            ],
            options={
                'db_table': 'document_statuses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelErpStatuses',
            fields=[
                ('status_id', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID статуса')),
                ('status_description', models.CharField(default='Нет описания', max_length=512, verbose_name='Статус ERP')),
            ],
            options={
                'db_table': 'erp_statuses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelIncomeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_ware_code', models.CharField(db_column='internal_warecode', editable=False, max_length=256, verbose_name='Артикул товара')),
                ('contractor_ware_count', models.FloatField(db_column='internal_warecount', default=0, editable=False, verbose_name='Количество')),
                ('contractor_cis', models.CharField(editable=False, max_length=256, verbose_name='КИЗ/КИТУ Контрагента')),
            ],
            options={
                'db_table': 'income_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelIncomes',
            fields=[
                ('guid', models.CharField(default=uuid.UUID('01a278fa-e181-4b71-9fd2-6f07c2bf1515'), editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='GUID Прихода')),
                ('internal_document_number', models.CharField(editable=False, max_length=128, verbose_name='Внутренний номер документа')),
                ('external_document_number', models.CharField(editable=False, max_length=128, verbose_name='Номер документа контрагента')),
                ('document_date', models.DateField(default=datetime.date(2000, 1, 1), editable=False, verbose_name='Дата документа')),
                ('document_fobj', models.CharField(editable=False, max_length=64, verbose_name='Указатель')),
            ],
            options={
                'db_table': 'incomes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelMarkTypes',
            fields=[
                ('id', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False, verbose_name='ID Вида Маркировки')),
                ('description', models.CharField(default='Нет описания вида', max_length=512, verbose_name='Описание вида маркировки')),
                ('hs_flag', models.CharField(default='HS:NONE', max_length=64, verbose_name='Вид продукции ВМС')),
                ('ts_group_code', models.IntegerField(default=-1, verbose_name='ID Системы "Честный знак"')),
            ],
            options={
                'db_table': 'mark_types',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelOrders',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.UUID('c1d1b7cd-c9f5-4059-b432-b4fa318ab386'), editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='GUID Заказа')),
                ('order_status', models.BooleanField(default=True, verbose_name='Заказ завершен')),
                ('order_number', models.CharField(max_length=150, verbose_name='Номер заказа')),
                ('delivery_date', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата заказа')),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelWares',
            fields=[
                ('ware_guid', models.CharField(db_column='ware_guid', default=uuid.UUID('b51ffb5f-0cd5-4169-a594-89b9acd2a1e9'), max_length=64, primary_key=True, serialize=False, verbose_name='GUID Продукции')),
                ('ware_code', models.CharField(max_length=32, verbose_name='Артикул продукции')),
                ('ware_name', models.CharField(max_length=150, verbose_name='Наименование продукции')),
                ('ware_data', models.CharField(max_length=128, verbose_name='Данные ШК/Кода продукции')),
                ('marked', models.BooleanField(default=0, verbose_name='Пометка удаления')),
                ('lvl1_qty', models.FloatField(default=0, verbose_name='Коэффициент упаковки')),
                ('weight', models.BooleanField(db_column='weigth', default=0, verbose_name='Весовой')),
            ],
            options={
                'db_table': 'wares',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelWaresGtins',
            fields=[
                ('guid', models.CharField(default=uuid.UUID('c439206d-0ef3-40bd-9d53-adb3f30a5a47'), max_length=64, primary_key=True, serialize=False, verbose_name='GUID Записи')),
                ('ware_gtin', models.CharField(editable=False, max_length=64, verbose_name='GTIN Продукции')),
                ('ts_group_code', models.IntegerField(editable=False, verbose_name='ID Вида Маркировки')),
            ],
            options={
                'db_table': 'wares_gtins',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelWaresMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата начала действия')),
                ('hs_flag', models.CharField(default='HS:NONE', max_length=64, verbose_name='Вид продукции ВМС')),
            ],
            options={
                'db_table': 'wares_marks',
                'managed': False,
            },
        ),
    ]
