from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import UserProfile
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models  import  User
from  django.contrib.auth  import  login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db import  transaction
from datetime import datetime
import  json
from django.http import JsonResponse
from datetime import datetime
import logging

@csrf_exempt
@api_view(['POST'])
def register_user(request):
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



@csrf_exempt
@api_view(['POST'])
def login_user(request):
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
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    else:
        return Response({'error': 'Invalid  email and password '}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
def logout_user(request):
    logout(request)  # ends session
    return Response({'message': 'Logged out successfully'}, status=200)


