from django.urls import path
from .views import PatientCreateAPI, PatientListAPI, PatientDetailAPI, PatientUpdateAPI, PatientDeleteAPI

urlpatterns = [
    path('add/', PatientCreateAPI.as_view(), name='add-patient'),
    path('list/', PatientListAPI.as_view(), name='list-patients'),
    path('<int:patient_id>/', PatientDetailAPI.as_view(), name='patient-detail'),
    path('<int:patient_id>/update/', PatientUpdateAPI.as_view(), name='update-patient'),
    path('<int:patient_id>/delete/', PatientDeleteAPI.as_view(), name='delete-patient'),
] 