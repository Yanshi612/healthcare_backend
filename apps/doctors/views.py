from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(APIView):
    """
    GET  /api/doctors/ - List all doctors (any authenticated user).
    POST /api/doctors/ - Create a new doctor record.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(
            {"count": doctors.count(), "doctors": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Doctor created successfully.", "doctor": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    """
    GET    /api/doctors/<id>/ - Retrieve a specific doctor.
    PUT    /api/doctors/<id>/ - Update a doctor record.
    DELETE /api/doctors/<id>/ - Delete a doctor record.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DoctorSerializer(doctor)
        return Response({"doctor": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Doctor updated successfully.", "doctor": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        doctor.delete()
        return Response(
            {"message": "Doctor deleted successfully."},
            status=status.HTTP_200_OK,
        )
