
from rest_framework.decorators import  api_view,permission_classes
from rest_framework.permissions  import  IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from  ..models  import  Appointments
from  django.views.decorators.csrf import csrf_protect

@csrf_protect
@api_view(['post'])
@permission_classes([IsAuthenticated])
def update_request_status(request,appointment_id):

    try:
        listed_appointments =  Appointments.objects.get(id=appointment_id)
    except  Appointments.DoesNotExist:
        return  Response({'message':f"appointment with  id {appointment_id} does not exist"},status=status.HTTP_404_NOT_FOUND)

    if listed_appointments.doctor_id.user  != request.user:
        return  Response({'message':'You are not the owner you can not edit the appointment '},status=status.HTTP_400_BAD_REQUEST)

    status_value =  request.data.get('status')
    if status_value  not in ['1','2']:
        return  Response({'message':'Invalid status value'},status=status.HTTP_400_BAD_REQUEST)

    listed_appointments.status =  int(status_value)
    listed_appointments.save()

    return  Response({'message':'Appointment status updated successfully'},status=status.HTTP_200_OK)

    
