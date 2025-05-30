
from django.views.decorators.csrf import  csrf_exempt
from  rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
from ..models import FamilyMember
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from  django.views.decorators.cache  import  never_cache
from  django.views.decorators.csrf import  csrf_protect

def get_all_descendants(user):

    descendants =[]
    queue = [user]

    while queue:
        
        current_user  =  queue.pop(0)
        direct_family=   FamilyMember.objects.filter(parent_user=current_user)
        descendants.extend(direct_family)
        queue.extend([member.user for member in  direct_family])
    return  descendants

@csrf_protect
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@never_cache
def edit_family_members(request,member_id):

    data =  request.data
    user  =  request.user
    all_descendants  =  get_all_descendants(user)
    try:
        family_member =  FamilyMember.objects.get(uuid=member_id)
        if family_member not  in  all_descendants:
            return Response({'error': 'Unauthorized to edit this family member'}, status=status.HTTP_403_FORBIDDEN)

        family_user =  family_member.user

        # update fields provide in the request
        if 'username' in  data:
            family_user.username =  data['username']
            family_member.username =  data['username']

        if 'email' in data:
            family_user.email =data['email']
            family_member.email =data['email']

        if  'password' in data and data['password'].strip():
            family_user.password=make_password(data['password'])
            family_member.password= family_user.password

        if 'dob' in  data:
            family_member.dob =  datetime.strptime(data['dob'],'%Y-%m-%d').date()

        if 'gender' in data:
            family_member.gender = data['gender']

        if 'phone_number' in data:
            family_member.phone_number=data['phone_number']

        family_user.save()
        family_member.save()

        return  Response({'message':'User profile is updated'},status=status.HTTP_200_OK)
    
    except FamilyMember.DoesNotExist:
        return Response({'error': 'Family member not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
