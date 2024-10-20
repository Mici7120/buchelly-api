from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AppointmentSerializer
from .models import Appointment

# Create your views here.
class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()