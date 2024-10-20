from rest_framework import serializers
from .models import Appointment, Blockeddatetime
from django.utils import timezone

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        startdatetime = data.get('startdatetime')
        enddatetime = data.get('enddatetime')

        # Validar que la fechas no sean pasadas
        if startdatetime < timezone.now():
            raise serializers.ValidationError("La fecha de inicio ya paso.")
        
        if enddatetime < timezone.now():
            raise serializers.ValidationError("La fecha de final ya paso.")
        
        # Validar que la fecha de inicio no sea mayor que la fecha final
        if startdatetime > enddatetime:
            raise serializers.ValidationError("La fecha de inicio no puede ser posterior a la fecha final.")
        
        if startdatetime == enddatetime:
            raise serializers.ValidationError("La fecha de inicio no puede ser igual a la fecha final.")
        
        # Validar si las fechas estan un intervalo bloqueado
        blocked_intervals = Blockeddatetime.objects.filter(
            startdatetime__lte=startdatetime,
            enddatetime__gt=startdatetime
        ) | Blockeddatetime.objects.filter(
            startdatetime__lt=enddatetime,
            enddatetime__gte=enddatetime
        ) | Blockeddatetime.objects.filter(
            startdatetime__gte=startdatetime,
            enddatetime__lte=enddatetime
        )

        if blocked_intervals.exists():
            raise serializers.ValidationError("No se puede crear una cita que se solape con un horario bloqueado.")
        
        # Validar si las fechas estan en un cita existente
        appointments = Appointment.objects.filter(
            startdatetime__lte=startdatetime,
            enddatetime__gt=startdatetime
        ) | Appointment.objects.filter(
            startdatetime__lt=enddatetime,
            enddatetime__gte=enddatetime
        ) | Appointment.objects.filter(
            startdatetime__gte=startdatetime,
            enddatetime__lte=enddatetime
        )

        if appointments.exists():
            raise serializers.ValidationError("No se puede crear una cita que se solape con otra cita.")
        
        return data

class BlockeddatetimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockeddatetime
        fields = '__all__'