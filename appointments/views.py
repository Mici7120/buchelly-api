from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AppointmentSerializer, BlockeddatetimeSerializer
from .models import Appointment, Blockeddatetime
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from jobs.views import schedule_reminder_emails

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
        schedule_reminder_emails(appointment=appointment)
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

    @action(detail=False, methods=["get"])
    def recent(self, request, pk=None):
        recent_30 = timezone.now() - timedelta(days=30)
        appointments = Appointment.objects.filter(startdatetime__gte=recent_30)
        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def date_range(self, request, pk=None):
        start_date = request.data.get('startdatetime')
        end_date = request.data.get('enddatetime')

        appointments = Appointment.objects.filter(startdatetime__gte=start_date, enddatetime__lte=end_date)
        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data)
    
    @action(detail=True, methods=["put"])
    def edit_appointment(self, request, pk=None):
        try:
            appointment = Appointment.objects.filter(appointmentid=pk).first()
            new_start = request.data.get("startdatetime")
            new_end = request.data.get("enddatetime")

            conflict_appointments = Appointment.objects.filter(
                startdatetime__lt=new_end, enddatetime__gt=new_start, status=True
            ).exclude(appointmentid=pk)
            conflict_blocked = Blockeddatetime.objects.filter(
                startdatetime__lt=new_end, enddatetime__gt=new_start, status=True
            )

            if conflict_appointments.exists() or conflict_blocked.exists():
                return Response({"error": "El horario no está disponible."}, status=status.HTTP_400_BAD_REQUEST)

            appointment.startdatetime = new_start
            appointment.enddatetime = new_end
            appointment.save()

            send_mail(
                subject="Creaciones Buchelly - Cita actualizada",
                message=f"Su cita ha sido actualizada.\n\nNuevos detalles de la cita:\n\nID: {appointment.appointmentid}\nFecha y hora: {appointment.startdatetime}",
                recipient_list=[appointment.appuserid.email],
                from_email=None
            )

            send_mail(
                subject="Cita actualizada por el usuario",
                message=f"El usuario {appointment.appuserid.email} ha actualizado la cita ID: {appointment.appointmentid}. Nuevas fechas: {appointment.startdatetime} a {appointment.enddatetime}.",
                recipient_list=["admin@example.com"],
                from_email=None
            )

            return Response({"message": "Cita actualizada exitosamente."}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({"error": "Cita no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def cancel_appointment(self, request):
        appointment_id = request.data.get("appointmentid")

        try:
            appointment = Appointment.objects.get(appointmentid=appointment_id, status=True)
            appointment.status = False 
            appointment.save()

            send_mail(
                subject="Creaciones Buchelly - Cita cancelada",
                message=f"Su cita con ID {appointment.appointmentid} ha sido cancelada exitosamente.",
                recipient_list=[appointment.appuserid.email],
                from_email=None
            )

            """     send_mail(
                subject="Cita cancelada por el usuario",
                message=f"El usuario {appointment.appuserid.email} ha cancelado la cita ID: {appointment.appointmentid}.",
                recipient_list=["admin@example.com"],
                from_email=None
            ) """

            return Response({"message": "Cita cancelada exitosamente."}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({"error": "Cita no encontrada o ya está cancelada."}, status=status.HTTP_404_NOT_FOUND)

class BlockeddatetimeView(viewsets.ModelViewSet):
    serializer_class = BlockeddatetimeSerializer
    queryset = Blockeddatetime.objects.all()