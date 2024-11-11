# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid


class Appointment(models.Model):
    #appointmentid = models.UUIDField(db_column='AppointmentId', primary_key=True, default=uuid.uuid4, editable=False)  # Field name made lowercase.
    appointmentid = models.CharField(db_column='AppointmentId', primary_key=True, blank=True, editable=False)  # Prueba actualizar citas
    appuserid = models.ForeignKey('appuser.AppUser', models.DO_NOTHING, db_column='user_id')  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='StartDatetime', unique=True)  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='EndDatetime', unique=True)  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', default=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Appointment'


class Blockeddatetime(models.Model):
    blockeddatetimeid = models.CharField(db_column='BlockedDatetimeId', primary_key=True, max_length=36, blank=True)  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='StartDatetime')  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='EndDatetime')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', default=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'BlockedDatetime'
