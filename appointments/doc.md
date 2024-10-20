# Endpoints

## `/appointments`

### Metodos Disponibles:

- `GET` : Obtiene todas las citas
- `POST` : Crea una nueva cita

### Ejemplo de Peticion GET:

```bash
curl -X GET http://localhost:8000/appointments/
```

### Ejemplo de Peticion POST:

```bash
curl -X POST http://localhost:8000/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
        "appointmentid": "some-unique-id",
        "appuserid": 1,
        "startdatetime": "2023-10-01T10:00:00Z",
        "enddatetime": "2023-10-01T11:00:00Z",
        "status": true
      }'
```

## `/appointments/get_not_available_schedules/`

### Metodos Disponibles:

- `GET` : Obtiene los horarios no disponibles (citas y horarios bloqueados)

### Ejemplo de Peticion GET:

```bash
curl -X GET http://localhost:8000/appointments/get_not_available_schedules/
```

## `/blockeddatetimes/`

### Metodos Disponibles:

- `GET` : Obtiene todos los horarios bloqueados
- `POST` : Crea un nuevo horario bloqueado

### Ejemplo de Peticion GET:

```bash
curl -X GET http://localhost:8000/blockeddatetimes/
```

### Ejemplo de Peticion POST:

```bash
curl -X POST http://localhost:8000/blockeddatetimes/ \
  -H "Content-Type: application/json" \
  -d '{
        "blockeddatetimeid": "some-unique-id",
        "startdatetime": "2023-10-01T10:00:00Z",
        "enddatetime": "2023-10-01T11:00:00Z",
        "status": true
      }'
```

# Modelos

## Appointment

Representa una cita en el sistema.

### Campos:

- `appointmentid` : CharField (Primary Key, UUID)
- `appuserid` : IntegerField (Foreign Key, Referencia a `AppUser`)
- `startdatetime` : DateTimeField (Fecha y hora de inicio de la cita)
- `enddatetime` : DateTimeField (Fecha y hora de fin de la cita)
- `status` : BooleanField (Estado de la cita)

## BlockedDateTime

Representa un horario bloqueado en el sistema.

### Campos:

- `blockeddatetimeid` : CharField (Primary Key, UUID)
- `startdatetime` : DateTimeField (Fecha y hora de inicio del horario bloqueado)
- `enddatetime` : DateTimeField (Fecha y hora de fin del horario bloqueado)
- `status` : BooleanField (Estado del horario bloqueado)

## Serializadores

## AppointmentSerializer

Serializador para el modelo `Appointment`.

### Validaciones:

- Las fechas no deben ser pasadas.
- La fecha de inicio no puede ser posterior a la fecha final.
- La fecha de inicio no puede ser igual a la fecha final.
- Las fechas no deben solaparse con horarios bloqueados.
- Las fechas no deben solaparse con otras citas.
