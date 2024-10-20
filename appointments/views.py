from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AppointmentSerializer, BlockeddatetimeSerializer
from .models import Appointment, Blockeddatetime
from django.utils import timezone
from django.core.mail import send_mail

# Create your views here.
class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def perform_create(self, serializer):
        appointment = serializer.save()
        send_mail(
            subject="Creaciones Buchelly - Cita creada",
            message= f"Su cita ha sido creada exitosamente.\n\nDetalles de la cita:\n\nID: {appointment.appointmentid}\nFecha y hora: {appointment.startdatetime}",
            recipient_list=[appointment.appuserid.email],
            from_email=None
        )
        return Response(appointment, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def get_not_available_schedules(self, request, pk=None):
        timenow = timezone.now()
        blocked_datetimes = Blockeddatetime.objects.filter(
            status=True,
            enddatetime__gt=timenow
        ).values("startdatetime", "enddatetime")
        appointments = Appointment.objects.filter(enddatetime__gt=timenow).values("startdatetime", "enddatetime")

        not_available_schedules = list(blocked_datetimes) + list(appointments)

        return Response(not_available_schedules)

class BlockeddatetimeView(viewsets.ModelViewSet):
    serializer_class = BlockeddatetimeSerializer
    queryset = Blockeddatetime.objects.all()