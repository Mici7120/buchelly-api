# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Userrole(models.Model):
    userroleid = models.CharField(db_column='UserRoleId', primary_key=True, max_length=36)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    status = models.BooleanField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRole'


class Appuser(models.Model):
    appuserid = models.CharField(db_column='AppUserId', primary_key=True, max_length=36)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=250)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=250)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=300)  # Field name made lowercase.
    userroleid = models.ForeignKey('Userrole', models.DO_NOTHING, db_column='UserRoleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AppUser'


class Appointment(models.Model):
    appointmentid = models.CharField(db_column='AppointmentId', primary_key=True, max_length=36)  # Field name made lowercase.
    appuserid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='AppUserId')  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='StartDatetime')  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='EndDatetime')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Appointment'


class Blockeddatetime(models.Model):
    blockeddatetimeid = models.CharField(db_column='BlockedDatetimeId', primary_key=True, max_length=36)  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='StartDatetime')  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='EndDatetime')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BlockedDatetime'
