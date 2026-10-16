from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model — used for create, update, and detail views."""

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "blood_group",
            "address",
            "phone",
            "medical_history",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate_age(self, value):
        if value <= 0 or value > 150:
            raise serializers.ValidationError("Age must be between 1 and 150.")
        return value

    def validate_phone(self, value):
        cleaned = value.replace(" ", "").replace("-", "").replace("+", "")
        if not cleaned.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(cleaned) < 7 or len(cleaned) > 15:
            raise serializers.ValidationError("Phone number must be between 7 and 15 digits.")
        return value
