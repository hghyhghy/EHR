
from rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework.permissions  import IsAuthenticated
from  rest_framework.response  import  Response
from  rest_framework import  status
from  ..models  import  DoctorProfile,Appointments,UserProfile,tests,medicines
from  django.utils.dateparse import  parse_datetime
from  django.views.decorators.csrf import  csrf_protect
from django.core.signing import  loads,BadSignature
import  mimetypes

ALLOWED_MIME_TYPES = ['application/pdf', 'image/jpeg', 'image/png']

def is_valid_file(file):
    mime_tye,_ =  mimetypes.guess_type(file.name)
    return  mime_tye in ALLOWED_MIME_TYPES

@csrf_protect
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_appointment(request,doctor_id):
    user  =  request.user

    try:
        user_id  =  user.profile
    except  UserProfile.DoesNotExist:
        return  Response({'message':'User with this id does not exist'},status=status.HTTP_404_NOT_FOUND)

    venue  =  request.data.get('venue')
    scheduled_on  =request.data.get('scheduled_on')

    if not all([venue,scheduled_on]):
        return  Response({'message':'Those fields are required'},status=status.HTTP_400_BAD_REQUEST)

    try:
        real_doctor_id =  loads(doctor_id)
        doctor =  DoctorProfile.objects.get(id=real_doctor_id)

    except  (BadSignature,DoctorProfile.DoesNotExist):
        return  Response({'message':'Doctor with this id does not exist'},status=status.HTTP_404_NOT_FOUND)

    try:
        scheduled_datetime  =  parse_datetime(scheduled_on)
        if not scheduled_datetime:
            raise ValueError
        
    except ValueError:
        return  Response({'message':'Need scheduled time  in ISO format'},status=status.HTTP_400_BAD_REQUEST)
    
    reports_file   = request.FILES.get('reports')
    prescription_file   = request.FILES.get('prescription_file')

    if reports_file and not is_valid_file(reports_file):
        return  Response({'message':'Invalid reports file format allowed only  PDF,JPG,PNG'},status=status.HTTP_400_BAD_REQUEST)

    if prescription_file and not is_valid_file(prescription_file):
        return  Response({'message':'Invalid prescription file format allowed file format is PDF,JPG,PNG'},status=status.HTTP_400_BAD_REQUEST)
    
    test_id = request.data.get('prescribed_tests')
    medicine_id = request.data.get('prescribed_medicines')

    prescribed_test = None
    prescribed_medicine = None

    if test_id:
        try:
            prescribed_test=tests.objects.get(id=test_id)

        except  tests.DoesNotExist:
            return  Response({'message':'Test could not be found'},status=status.HTTP_400_BAD_REQUEST)

    if medicine_id:
        try:
            prescribed_medicine = medicines.objects.get(id=medicine_id)
        except  medicines.DoesNotExist:
            return  Response({'message':'Medicines could not be found'},status=status.HTTP_400_BAD_REQUEST)


    appointment  =  Appointments.objects.create(

        user_id=user.profile,
        doctor_id=doctor,
        category_id  =  doctor.category_id,
        scheduled_on=scheduled_datetime,
        venue=venue,
        reports=reports_file,
        prescription_file=prescription_file,
        prescribed_tests=prescribed_test,
        prescribed_medicines=prescribed_medicine
        
    )

    return  Response({
        'message':'Appointment booked successfully',
        'appointment_id':appointment.id,
        'user_id':user.id,
        
    },status=status.HTTP_201_CREATED)
