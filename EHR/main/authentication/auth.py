from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import UserProfile
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models  import  User
from  django.contrib.auth  import  login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from django.db import  transaction
from datetime import datetime
import  json
from django.http import JsonResponse
from datetime import datetime
import logging
from  django.views.decorators.csrf import  csrf_protect
from  rest_framework.decorators import  throttle_classes
from ..throttling import  RegisterRateThrottle,LoginRateThrottle
import requests


def verify_captcha(captcha_response):
    secret_key = '6LetAlQrAAAAAGYXwAiEApC0eqzks-vsbc_24RxJ'  # From Google reCAPTCHA dashboard
    payload = {
        'secret': secret_key,
        'response': captcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = r.json()
    return result.get('success', False)


@api_view(['POST'])
@throttle_classes([RegisterRateThrottle])
def register_user(request):
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'}, status=status.HTTP_403_FORBIDDEN)


    data = request.data
    print("Received data:", data)  # debug

    required_fields = ['username',  'email', 'gender', 'dob', 'phone_number', 'password']
        
    for field in required_fields:
        if not data.get(field):
            print(f"Missing field: {field}")
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        dob_value = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        print("Parsed DOB:", dob_value)

        with transaction.atomic():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
                #create_user() already hashes the password internally. Manually calling make_password() here will double-hash the password, so the password stored won't match the plain text password during authenticate(). that hwy when we call the 
                #login then it called the double hashed password leading to the unauthorized error .. fixed 


            )
            profile = UserProfile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                password=user.password,
                dob=dob_value,
                gender=data['gender'],
                phone_number=data['phone_number']
            )
            print("UserProfile created:", profile)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        import traceback
        traceback.print_exc()  # full traceback in terminal
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_protect
@throttle_classes([LoginRateThrottle])
@api_view(['POST'])
def login_user(request):
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'}, status=status.HTTP_403_FORBIDDEN)
    captcha_response  =  request.data.get('recaptcha')
    if not captcha_response or not verify_captcha(captcha_response):
        return Response({'error': 'CAPTCHA validation failed.'}, status=400)

    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({'error': 'email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user  =  User.objects.get(email=email)
    except  User.DoesNotExist:
        return  Response({'message':'Invalid email  or password'}, status=status.HTTP_404_NOT_FOUND)

    user = authenticate(username=user.username, password=password)

    if user is not None:
        login(request,user)
        return Response({'message': 'Login successful (session set)'})
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)  # ends session
    return Response({'message': 'Logged out successfully'}, status=200)


