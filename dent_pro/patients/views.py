from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer
from .models import Patient
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PatientCreateAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PatientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Patient created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PatientListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True, context={'request': request})
        return Response({
            'status': True,
            'data': serializer.data
        })

class PatientDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        serializer = PatientSerializer(patient, context={'request': request})
        return Response({
            'status': True,
            'data': serializer.data
        })

class PatientUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        serializer = PatientSerializer(patient, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Patient updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PatientDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        patient.delete()
        return Response({
            'status': True,
            'message': 'Patient deleted successfully'
        })
