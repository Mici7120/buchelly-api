from rest_framework import serializers
from .models import AppUser
from userrole.serializer import UserRoleSerializer

class AppUserSerializer(serializers.ModelSerializer):
  userroleid = UserRoleSerializer()
  class Meta:
    model = AppUser
    fields = ('id', 'fullname', 'email', 'userroleid')