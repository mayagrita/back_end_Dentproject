from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer
from .serializers import NoteSerializer
from .models import Patient
from .models import Note
from rest_framework import generics
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




class AddNoteAPI(generics.CreateAPIView):
    serializer_class = NoteSerializer

    def create(self, request, *args, **kwargs):
        patient_id = self.kwargs.get("patient_id")
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(patient=patient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PatientNotesListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        notes = Note.objects.filter(patient=patient)
        serializer = NoteSerializer(notes, many=True)
        return Response({
            'status': True,
            'data': serializer.data
        })

class DeleteNoteAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, patient_id, note_id):
        patient = get_object_or_404(Patient, id=patient_id)
        note = get_object_or_404(Note, id=note_id, patient=patient)
        note.delete()
        return Response({
            'status': True,
            'message': 'Note deleted successfully'
        })
