from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AppointmentSerializer, BlockeddatetimeSerializer
from .models import Appointment, Blockeddatetime
from django.utils import timezone

# Create your views here.
class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

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