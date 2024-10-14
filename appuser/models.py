from django.db import models
from django.utils import timezone

class AppUser(models.Model):
    appuserid = models.CharField(db_column='id', primary_key=True, max_length=36)  # Field name made lowercase.
    fullname = models.CharField(db_column='full_name', max_length=250)  # Field name made lowercase.
    email = models.CharField(db_column='email', max_length=250)  # Field name made lowercase.
    password = models.CharField(db_column='password', max_length=300)  # Field name made lowercase.
    userroleid = models.ForeignKey('userrole.UserRole', models.DO_NOTHING, db_column='user_role_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AppUser'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'PasswordResetToken'
    def is_expired(self):
        return timezone.now() > self.expiration_date

    def __str__(self):
        return f"Token for {self.user.email}"