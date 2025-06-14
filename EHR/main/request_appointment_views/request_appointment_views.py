
from  rest_framework.decorators  import  api_view,permission_classes,authentication_classes
from rest_framework.permissions  import  IsAuthenticated
from  ..models  import  Appointments
from rest_framework.response import  Response
from  rest_framework import  status
from  django.views.decorators.csrf import  csrf_protect

@csrf_protect
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def listed_appointments(request):

    doctor  =  request.user.doctor_profile
    appointments  =  Appointments.objects.filter(doctor_id =  doctor)

    data =[]
    for app   in appointments:
        patient  = app.user_id

        data.append({
            'Application_id':app.id,
            'Appointed_doctor':doctor.username,
            'Degree':doctor.degree,
            'category':doctor.category_id.category_name,
            'name':patient.username,
            'dob':patient.dob,
            'gender':patient.gender,
            'phone_number':patient.phone_number,
            'scheduled_on':app.scheduled_on,
            'venue':app.venue,
            'status':app.status
        });

    return  Response(data,  status=status.HTTP_200_OK)