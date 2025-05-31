
from django.views.decorators.csrf import  csrf_exempt
from  rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
from ..models import FamilyMember,UserProfile
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
def edit_family_members(request, member_id):
    from ..models import UserProfile  # Import inside view to avoid circular imports
    data = request.data
    user = request.user
    all_descendants = get_all_descendants(user)

    try:
        family_member = FamilyMember.objects.get(uuid=member_id)
        if family_member not in all_descendants:
            return Response({'error': 'Unauthorized to edit this family member'}, status=status.HTTP_403_FORBIDDEN)

        family_user = family_member.user

        # Update fields provided in the request
        if 'username' in data:
            family_user.username = data['username']
            family_member.username = data['username']

        if 'email' in data:
            family_user.email = data['email']
            family_member.email = data['email']

        if 'password' in data and data['password'].strip():
            hashed_pw = make_password(data['password'])
            family_user.password = hashed_pw
            family_member.password = hashed_pw

        if 'dob' in data:
            dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            family_member.dob = dob

        if 'gender' in data:
            family_member.gender = data['gender']

        if 'phone_number' in data:
            family_member.phone_number = data['phone_number']

        # Save user and family_member
        family_user.save()
        family_member.save()

        # ✅ Update corresponding UserProfile if exists
        try:
            user_profile = UserProfile.objects.get(user=family_user)
            if 'username' in data:
                user_profile.username = data['username']
            if 'email' in data:
                user_profile.email = data['email']
            if 'password' in data and data['password'].strip():
                user_profile.password = hashed_pw
            if 'dob' in data:
                user_profile.dob = dob
            if 'gender' in data:
                user_profile.gender = data['gender']
            if 'phone_number' in data:
                user_profile.phone_number = data['phone_number']
            user_profile.save()
        except UserProfile.DoesNotExist:
            pass  # If no user profile exists, skip it

        return Response({'message': 'Family member and profile updated successfully'}, status=status.HTTP_200_OK)

    except FamilyMember.DoesNotExist:
        return Response({'error': 'Family member not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
