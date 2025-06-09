
import  re
from  django.contrib.auth.models import  User
from  ..models import  DoctorProfile
from rest_framework.decorators  import  api_view
from rest_framework.response import  Response
from  rest_framework import  status

EMAIL_REGEX = r"(^[\w\.-]+@[\w\.-]+\.\w{2,4}$)"

@api_view(['POST'])
def reset_doctor_password(request):

    email =  request.data.get('email')
    password= request.data.get('password')

    if not email  or not re.match(EMAIL_REGEX,email) or not password:
        return  Response({'message':'Both email  and password fields are required'},status=status.HTTP_400_BAD_REQUEST)

    try:
        user=  User.objects.get(email=email)
        user.set_password(password)
        user.save()

        try:
            doctor_profile=  DoctorProfile.objects.get(email=email)
            doctor_profile.password=user.password
            doctor_profile.save()

        except  DoctorProfile.DoesNotExist:
            pass
        return Response({'message':'password reset successfully'},status=status.HTTP_200_OK)

    except  User.DoesNotExist:
        return  Response({'message':f"Doctor with email{email} does not exist"},status=status.HTTP_404_NOT_FOUND)
        