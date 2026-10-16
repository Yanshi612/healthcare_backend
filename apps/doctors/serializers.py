from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model."""

    class Meta:
        model = Doctor
        fields = (
            "id",
            "name",
            "specialization",
            "experience_years",
            "email",
            "phone",
            "hospital",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_experience_years(self, value):
        if value < 0 or value > 70:
            raise serializers.ValidationError("Experience years must be between 0 and 70.")
        return value

    def validate_phone(self, value):
        cleaned = value.replace(" ", "").replace("-", "").replace("+", "")
        if not cleaned.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(cleaned) < 7 or len(cleaned) > 15:
            raise serializers.ValidationError("Phone number must be between 7 and 15 digits.")
        return value

    def validate_email(self, value):
        instance = self.instance
        qs = Doctor.objects.filter(email=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value
