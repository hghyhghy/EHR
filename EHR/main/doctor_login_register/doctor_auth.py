from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import DoctorProfile,Category
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models  import  User
from  django.contrib.auth  import  login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db import  transaction
import  json
from django.http import JsonResponse
from datetime import datetime
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from  django.views.decorators.csrf import  csrf_protect
from  ..throttling import  RegisterRateThrottle,LoginRateThrottle
from  rest_framework.decorators import throttle_classes
import  requests

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
def register_view_of_doctors(request):
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'}, status=status.HTTP_403_FORBIDDEN)
    data  =  request.data

    required_fields = ['username','email','password','category','degree','dob','gender','phone_number']
    for fields in  required_fields:
        if not data.get(fields):
            print(f"Missing field {fields}")
            return Response({'message':f"Missing the required field {fields}"},status=status.HTTP_400_BAD_REQUEST)
        
    try:
        category   =  Category.objects.get(id= data['category'])
    except  Category.DoesNotExist:
        return Response({'message':"Category Does not exist"},status=status.HTTP_400_BAD_REQUEST)


    try:
        dob_value =  datetime.strptime(data['dob'], '%Y-%m-%d').date()
        with transaction.atomic():
            user =  User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )


            doctor =  DoctorProfile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                password=user.password,
                category_id=category,
                degree=data['degree'],
                dob=dob_value,
                gender=data['gender'],
                phone_number=data['phone_number']
            )

        return  Response({'message':'Doctor profile created'},status=status.HTTP_201_CREATED)

    except  Exception as e:
        import traceback
        traceback.print_exc()  # full traceback in terminal
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@throttle_classes([LoginRateThrottle])
def login_view_for_doctor(request):
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'}, status=status.HTTP_403_FORBIDDEN)
    capcha_response  =  request.data.get('recaptcha')
    if not capcha_response or not verify_captcha(capcha_response):
        return Response({'error': 'CAPTCHA validation failed.'}, status=400)

    data  =  request.data
    email = data.get('email')
    password=data.get('password')

    if not email or not password:
        return Response({'message':'Both fields are required'},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user =  User.objects.get(email=email)
    except User.DoesNotExist:
        return  Response({'message':'User does not exist with this email'},status=status.HTTP_404_NOT_FOUND)

    
    user=  authenticate(username=user.username,password=password)

    if user is not None:
        login(request,user)

        return Response({'message': 'Login successful (session set)'})
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_doctor(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=200)
