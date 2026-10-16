from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(APIView):
    """
    GET  /api/patients/ - List all patients created by the authenticated user.
    POST /api/patients/ - Create a new patient record.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response(
            {"count": patients.count(), "patients": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {"message": "Patient created successfully.", "patient": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    """
    GET    /api/patients/<id>/ - Retrieve a specific patient.
    PUT    /api/patients/<id>/ - Update a patient.
    DELETE /api/patients/<id>/ - Delete a patient.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Patient.objects.get(pk=pk, created_by=user)
        except Patient.DoesNotExist:
            return None

    def get(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient)
        return Response({"patient": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Patient updated successfully.", "patient": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        patient.delete()
        return Response(
            {"message": "Patient deleted successfully."},
            status=status.HTTP_200_OK,
        )
