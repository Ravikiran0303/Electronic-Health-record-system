from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Appointment, Doctor, Patient
from .prediction import predict_disease
from .serializers import AppointmentSerializer, DoctorSerializer, PatientSerializer


# Create your views here.


class DoctorView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            doctor = Doctor.objects.filter(docID=id)
            serializer = DoctorSerializer(doctor, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)

    def delete(self, request, id=None):
        doctor = Doctor.objects.filter(docID=id)
        doctor.delete()

        return Response({"status": "success", "data": True})


class PatientView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentView(APIView):
    def post(self, request):

        doctor = Doctor.objects.get(docID=request.data.get('docID'))
        patient = Patient.objects.get(patID=request.data.get('patID'))

        request.data._mutable = True
        request.data['docName'] = doctor.fName + ' ' + doctor.lName
        request.data['patName'] = patient.patName
        request.data._mutable = False

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)

    def put(self, request, id):
        appointment = Appointment.objects.get(id=id)
        appointment.status = True
        appointment.save()
        return Response({"status": "success", "data": appointment.status}, status.HTTP_200_OK)


@api_view(['GET'])
def getAppointmentDoc(self, id):
    appointment = Appointment.objects.filter(docID=id)
    serializer = AppointmentSerializer(appointment, many=True)
    return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)


@api_view(['GET'])
def getAppointmentPat(self, id):
    appointment = Appointment.objects.filter(patID=id)
    serializer = AppointmentSerializer(appointment, many=True)
    return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)


@api_view(['GET'])
def getCount(self):
    doctorCount = Doctor.objects.all().count()
    patientCount = Patient.objects.all().count()
    return Response({"status": "success", "docCount": doctorCount, "patCount": patientCount}, status.HTTP_200_OK)


@api_view(['GET'])
def clear(self):
    Doctor.objects.all().delete()
    Appointment.objects.alias().delete()
    Patient.objects.alias().delete()

    return Response({"status": "success"}, status.HTTP_200_OK)


@api_view(['GET'])
def get_symptoms(self):
    data = {'symptoms': list(predict_disease.symptoms_dict.keys())}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def predict_diseases(request):
    symptoms = request.data.get('symptoms')
    print(symptoms)
    if symptoms == "Symptoms":
        print("Please either write symptoms or you have written misspelled symptoms")
        return Response({"status": "failed", "msg": "Invalid symptoms"}, status.HTTP_400_BAD_REQUEST)
    else:
        data = predict_disease.predict(symptoms)
        print(data)
        return Response({"status": "success", "msg": data}, status.HTTP_200_OK)
