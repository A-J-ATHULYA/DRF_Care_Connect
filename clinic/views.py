from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDb, AppointmentDb
from clinic.serializer import Doctor_Serializer, Appointment_Serializer
from datetime import datetime, time, timedelta
from rest_framework import serializers

# Create your views here.

class DoctorListCreateView(APIView):
    def get(self, request):
        qs = DoctorDb.objects.all()
        serializer_instance = Doctor_Serializer(qs, many=True)
        return Response(data=serializer_instance.data)
    
    def post(self, request):
        form_data = request.data
        serializer_instance = Doctor_Serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
        
class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(DoctorDb, id=pk)
        serializer_instance = Doctor_Serializer(qs)
        return Response(data=serializer_instance.data)
    
    def put(self, request, pk):
        form_data = request.data
        doctor_object = get_object_or_404(DoctorDb, id=pk)
        serializer_instance = Doctor_Serializer(data=form_data, instance=doctor_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
    def delete(self, request, pk):
        doctor_obj = get_object_or_404(DoctorDb, id=pk)
        doctor_obj.delete
        return Response(data={"Message":"Deleted"})
         
         
class AppointmentListCreateView(APIView):
    def get(self, request):
        qs = AppointmentDb.objects.all()
        serializer_instance = Appointment_Serializer(qs, many=True)
        return Response(data=serializer_instance.data)
    
    def post(self, request):
        form_data = request.data
        serializer_instance = Appointment_Serializer(data=form_data)
        if serializer_instance.is_valid():
            #actual = serializer_instance.validated_data
            appointment_date  = serializer_instance.validated_data.get("Appointment_date")
            doctor_id = serializer_instance.validated_data.get("Doctor_id")
        
            last_appointment = AppointmentDb.objects.filter(
                Appointment_date = appointment_date,
                Doctor_id = doctor_id
            ).order_by("-Token_number").first()
        
#last_appointment = [anu 4658978 1(name) 2026-nov-2 8 12.15] 

            if last_appointment is None:
                form_data["Token_number"] = 1
                form_data["Appointment_time"] = time(10, 0)
            
            else:
                # next_token = last_appointment.Token_number + 1
                form_data["Token_number"] = last_appointment.Token_number + 1
                current_time =datetime.combine(appointment_date, last_appointment.Appointment_time)
                next_time = current_time + timedelta(minutes=15)
                
                #adding break time
                # if next_time.time() == time(12, 30) :
                #     next_time = datetime.combine(appointment_date, time(13, 30))  

                if next_time.time() == time(17, 0):
                    return Response(data={
                        "message":"booking completed"
                    })
                    # serializers.ValidationError("No slots available")

                    
                # form_data["Token_number"] = next_token
                form_data["Appointment_time"] = next_time
                
                
            qs = AppointmentDb.objects.create(**form_data)
            serializer_instance = Appointment_Serializer(qs)
            return Response(data={
                "Message" : "Booked Successfully",
                "Token Number" : form_data["Token_number"]
            })
            
        else:
            return Response(data=serializer_instance.errors)