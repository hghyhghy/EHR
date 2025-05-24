


from django.views.decorators.csrf import  csrf_exempt
from  rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import DoctorProfile
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])

def get_doctor_details(request):        
    doctors =  DoctorProfile.objects.all()
    doctor_list= []

    for doctor  in  doctors:
        doctor_list.append({
            
            'username':doctor.username,
            'email':doctor.email,
            'degree':doctor.degree,
            'category':doctor.category_id.category_name,
            'gender':doctor.gender,
            'phone_number':doctor.phone_number
        });

    return  Response(doctor_list, status=status.HTTP_200_OK)