import uuid

from django.conf import settings
from django.db import models

from apps.doctors.models import Doctor
from apps.patients.models import Patient


class PatientDoctorMapping(models.Model):
    """Represents an assignment of a doctor to a patient."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="doctor_mappings",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="patient_mappings",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assignments",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "patient_doctor_mappings"
        unique_together = ("patient", "doctor")  # prevent duplicate assignments
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.patient.name} → Dr. {self.doctor.name}"
