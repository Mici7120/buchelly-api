from django.urls import path, include
from rest_framework import routers
from appointments import views

router = routers.DefaultRouter()
router.register(r'appointments', views.AppointmentView, 'appointments')

urlpatterns = [
    path("api/v1/", include(router.urls))
]