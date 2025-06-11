
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from ..models import EmailOTP, UserSession

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    user_id =  request.data.get('user_id')
    otp =  request.data.get('otp')

    if not user_id or not  otp:
        return  Response({'message':'User id and otp is required'},status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
        otp_record =  EmailOTP.objects.filter(user=user,otp=otp).order_by('-created_at').first()

        if otp_record and otp_record.is_valid():

            existing_Session  =  UserSession.objects.filter(user=user)
            Session.objects.filter(session_key__in=[
                s.session_key for s in existing_Session
            ]).delete()
            existing_Session.delete()

            login(request,user)
            UserSession.objects.create(user=user,session_key =  request.session.session_key)

            return Response({'message':'Otp  verified and login successful'},status=status.HTTP_202_ACCEPTED)

        else:
            return  Response({'message':'Invalid or expired otp'},status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return  Response({'message':"Invalid user"},status=status.HTTP_400_BAD_REQUEST)

        

