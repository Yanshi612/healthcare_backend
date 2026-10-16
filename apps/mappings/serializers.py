from apps.doctors.serializers import DoctorSerializer
from apps.patients.serializers import PatientSerializer
from rest_framework import serializers

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for creating a patient-doctor mapping."""

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "assigned_by", "assigned_at")
        read_only_fields = ("id", "assigned_by", "assigned_at")

    def validate(self, attrs):
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError(
                {"detail": "This doctor is already assigned to this patient."}
            )
        return attrs


class PatientDoctorMappingDetailSerializer(serializers.ModelSerializer):
    """Serializer for reading mapping records with nested patient/doctor details."""

    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    assigned_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "assigned_by", "assigned_at")
