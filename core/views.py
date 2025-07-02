# core/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Patient, MedicalRecord
from .serializers import UserSerializer, PatientSerializer, MedicalRecordSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})

@api_view(["GET"])
@permission_classes([AllowAny])
def welcome(request):
    return Response({"message": "Welcome to the Hospital API!"})


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AddMedicalRecordView(APIView):
    def post(self, request):
        patient_id = request.data.get('patient')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)
        
        if patient.created_by != request.user and not request.user.is_superuser:
            return Response({'error': 'Not authorized'}, status=403)
        
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PatientMedicalRecordsView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        patient_id = self.kwargs['id']
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return MedicalRecord.objects.none()

        if patient.created_by != self.request.user and not self.request.user.is_superuser:
            return MedicalRecord.objects.none()
        
        return patient.records.all()
