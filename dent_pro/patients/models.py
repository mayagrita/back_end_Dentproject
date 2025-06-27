from django.db import models
from django.utils import timezone

class Patient(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    image = models.ImageField(upload_to='patients/', blank=True, null=True, verbose_name="Patient Image")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    def __str__(self):
        return self.name

class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    diagnosis_text = models.TextField(verbose_name="Diagnosis Text")
    xray_image = models.ImageField(upload_to='diagnosis/xrays/', blank=True, null=True, verbose_name="X-ray Image")
    model_image = models.ImageField(upload_to='diagnosis/models/', blank=True, null=True, verbose_name="Model Image")
    date = models.DateTimeField(default=timezone.now, verbose_name="Diagnosis Date")

    def __str__(self):
        return f"{self.patient.name} - {self.date.strftime('%Y-%m-%d')}"

class Note(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField(verbose_name="Note Text")
    date = models.DateTimeField(default=timezone.now, verbose_name="Note Date")

    def __str__(self):
        return f"{self.patient.name} - {self.date.strftime('%Y-%m-%d')}"