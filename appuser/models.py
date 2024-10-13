from django.db import models

class AppUser(models.Model):
    appuserid = models.CharField(db_column='AppUserId', primary_key=True, max_length=36)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=250)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=250)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=300)  # Field name made lowercase.
    userroleid = models.ForeignKey('userrole.UserRole', models.DO_NOTHING, db_column='UserRoleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AppUser'