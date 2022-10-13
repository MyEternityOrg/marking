import uuid

from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class ModelCheckStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True, editable=False, auto_created=True)
    status_name = models.CharField(max_length=128)
    finished = models.IntegerField(default=0)

    class Meta:
        db_table = 'check_statuses'
        managed = False


class ModelDocumentStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True, editable=False, auto_created=True)
    status_description = models.CharField(max_length=512)
    status_level = models.IntegerField(default=-1)

    class Meta:
        db_table = 'document_statuses'
        managed = False


class ModelErpStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True, editable=False, auto_created=True)
    status_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'erp_statuses'
        managed = False


class ModelMarkTypes(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, auto_created=True)
    description = models.CharField(max_length=512)
    hs_flag = models.CharField(max_length=64)
    ts_group_code = models.IntegerField(default=0)

    class Meta:
        db_table = 'mark_types'
        managed = False


class ModelContractors(models.Model):
    guid = models.CharField(primary_key=True, editable=False, default=uuid.uuid4, max_length=64)
    contractor_name = models.CharField(max_length=150)
    contractor_inn = models.CharField(max_length=32)
    contractor_count_whitelist = models.IntegerField(default=0)
    contractor_quality_whitelist = models.IntegerField(default=0)
    contractor_mrc_minimal = models.IntegerField(default=0)

    class Meta:
        db_table = 'contractors'
        managed = False


class ModelContractorContacts(models.Model):
    contractor_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE)
    email = models.CharField(primary_key=True, unique=True, max_length=128)
    name = models.CharField(max_length=512)

    class Meta:
        db_table = 'contractor_contacts'
        managed = False


class ModelDocuments(models.Model):
    guid = models.CharField(primary_key=True, editable=False, default=uuid.uuid4, max_length=64)
    contractor_guid = models.ForeignKey(ModelContractors, on_delete=models.CASCADE)
    order_guid = models.CharField(max_length=64, default=uuid.uuid4)
    income_guid = models.CharField(max_length=64, default=uuid.uuid4)
    document_date = models.DateField()
    document_number = models.CharField(max_length=128)
    document_name = models.CharField(max_length=512)
    document_id = models.CharField(max_length=128)
    check_status_id = models.ForeignKey(ModelCheckStatuses, on_delete=models.DO_NOTHING)
    whitelisted = models.IntegerField(editable=False)
    document_status_id = models.ForeignKey(ModelDocumentStatuses, on_delete=models.DO_NOTHING)
    erp_status_id = models.ForeignKey(ModelErpStatuses, on_delete=models.DO_NOTHING)
    allowed_grayzone = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'documents'
        managed = False
