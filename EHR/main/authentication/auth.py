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
from django.views.decorators.csrf import csrf_exempt
from django.db import  transaction
from datetime import datetime

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    from datetime import datetime
    import logging

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
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password'])
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
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        # This will show you the error message instead of a blank 500 page
        return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def logout_user(request):
    logout(request)  # ends session
    return Response({'message': 'Logged out successfully'}, status=200)
