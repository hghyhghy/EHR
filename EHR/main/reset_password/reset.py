
import  re
from  django.contrib.auth.models  import  User
from ..models import UserProfile
from  rest_framework.decorators  import  api_view,throttle_classes
from  rest_framework.response import  Response
from rest_framework import  status,throttling

EMAIL_REGEX = r"(^[\w\.-]+@[\w\.-]+\.\w{2,4}$)"

class  ResetRateThrottle(throttling.AnonRateThrottle):
    rate='5/minutes'

@api_view(['POST'])
def reset_password(request):
    email =  request.data.get('email')
    password = request.data.get('password')

    if not email or not re.match(EMAIL_REGEX,email) or not password:
        return  Response({'message':'Both email and password fields are required'},status=status.HTTP_400_BAD_REQUEST)

    
    try:
        user=  User.objects.get(email=email)
        user.set_password(password)
        user.save()

        try:
            user_profile =   UserProfile.objects.get(user=user)
            user_profile.password=user.password
            user_profile.save()

        except UserProfile.DoesNotExist:
            pass
        return  Response({'message':'Passoword reset successfully'},status=status.HTTP_200_OK)

    except  User.DoesNotExist:
        return  Response({'message':f"User with this email  {email} does not exist"})