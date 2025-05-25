
from rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework.permissions  import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from  rest_framework.response  import  Response
from  rest_framework import  status
from  ..models  import  DoctorProfile,Appointments,UserProfile
from  django.utils.dateparse import  parse_datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])


def request_appointment(requset,doctor_id):
    user  =  requset.user

    try:
        user_id  =  user.profile
    except  UserProfile.DoesNotExist:
        return  Response({'message':'User with this id does not exist'},status=status.HTTP_404_NOT_FOUND)

    venue  =  requset.data.get('venue')
    scheduled_on  =requset.data.get('scheduled_on')

    if not all([venue,scheduled_on]):
        return  Response({'message':'Those fields are required'},status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor =  DoctorProfile.objects.get(id=doctor_id)

    except  DoctorProfile.DoesNotExist:
        return  Response({'message':'Doctor with this id does not exist'},status=status.HTTP_404_NOT_FOUND)

    try:
        scheduled_datetime  =  parse_datetime(scheduled_on)
        if not scheduled_datetime:
            raise ValueError
        
    except ValueError:
        return  Response({'message':'Need scheduled time  in ISO format'},status=status.HTTP_400_BAD_REQUEST)

    appointment  =  Appointments.objects.create(

        user_id=user.profile,
        doctor_id=doctor,
        category_id  =  doctor.category_id,
        scheduled_on=scheduled_datetime,
        venue=venue,
        
    )

    return  Response({
        'message':'Appointment booked successfully',
        'appointment_id':appointment.id,
        'user_id':user.id
    },status=status.HTTP_201_CREATED)
