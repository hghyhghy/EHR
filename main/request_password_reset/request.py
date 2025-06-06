
import  re
from rest_framework.decorators  import   api_view,throttle_classes
from rest_framework.response import  Response
from rest_framework import  status,throttling
from django.contrib.auth.models import  User


EMAIL_REGEX = r"(^[\w\.-]+@[\w\.-]+\.\w{2,4}$)"
class ResetRateThrottle(throttling.AnonRateThrottle):
    rate = '5/minute' 
@api_view(['POST'])
def request_password_reset(request):
    email =  request.data.get('email')
    if not email or not re.match(EMAIL_REGEX,email):
        return  Response({'message':'Email  id is required'},status=status.HTTP_400_BAD_REQUEST)

    try:
        user=  User.objects.get(email=email)
        if (user):
            return  Response({
           'message': 'Email verified. Proceed to reset.',
            'user_id':user.id
        },status=status.HTTP_200_OK)
        else:
            return Response({'message':'Email  verification failed'},status=status.HTTP_404_NOT_FOUND)

    except  User.DoesNotExist:
        return  Response({'message':f"user this email {email} does not exist"},status=status.HTTP_404_NOT_FOUND)