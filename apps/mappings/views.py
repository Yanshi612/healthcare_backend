from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingDetailSerializer, PatientDoctorMappingSerializer


class MappingListCreateView(APIView):
    """
    GET  /api/mappings/ - Retrieve all patient-doctor mappings.
    POST /api/mappings/ - Assign a doctor to a patient.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.select_related("patient", "doctor", "assigned_by").all()
        serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
        return Response(
            {"count": mappings.count(), "mappings": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assigned_by=request.user)
            return Response(
                {"message": "Doctor assigned to patient successfully.", "mapping": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MappingByPatientView(APIView):
    """
    GET /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        # Validate patient exists
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        mappings = PatientDoctorMapping.objects.select_related(
            "patient", "doctor", "assigned_by"
        ).filter(patient=patient)

        serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
        return Response(
            {
                "patient_id": str(patient_id),
                "patient_name": patient.name,
                "count": mappings.count(),
                "mappings": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class MappingDeleteView(APIView):
    """
    DELETE /api/mappings/<id>/ - Remove a doctor from a patient (delete mapping by mapping ID).
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=pk)
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {"error": "Mapping not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        mapping.delete()
        return Response(
            {"message": "Doctor removed from patient successfully."},
            status=status.HTTP_200_OK,
        )
