import uuid

from django.db import models


class Doctor(models.Model):
    """Represents a doctor in the healthcare system."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(help_text="Years of experience")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    hospital = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "doctors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dr. {self.name} — {self.specialization}"
