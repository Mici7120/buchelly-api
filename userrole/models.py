from django.db import models

class UserRole(models.Model):
    userroleid = models.CharField(db_column='UserRoleId', primary_key=True, max_length=36)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    status = models.BooleanField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRole'
