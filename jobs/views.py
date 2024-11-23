from jobs.scheduler import scheduler
from django.core.mail import send_mail
from apscheduler.triggers.date import DateTrigger
from datetime import timedelta
import pytz

def schedule_reminder_emails(appointment):
    colombia_zone = pytz.timezone("America/Bogota")
    scheduler.add_job(
        lambda: send_mail(
            subject="Recordatorio de cita",
            message=f"No olvides que tu cita es mañana a las {appointment.startdatetime.astimezone(colombia_zone)}.",
            recipient_list=[appointment.appuserid.email],
            from_email=None
        ),
        trigger=DateTrigger(run_date=appointment.startdatetime - timedelta(days=1))
    )

    scheduler.add_job(
        lambda: send_mail(
            subject="Recordatorio de cita",
            message=f"No olvides que tu cita es hoy a las {appointment.startdatetime.astimezone(colombia_zone)}.",
            recipient_list=[appointment.appuserid.email],
            from_email=None
        ),
        trigger=DateTrigger(run_date=appointment.startdatetime - timedelta(minutes=30))
    )