from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from ..models import FamilyMember,UserProfile
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from  django.views.decorators.csrf import  csrf_protect

def recursively_find_the_main_user(user):
    # traverse to the top until we found the main user  
    while True:
        try:
            family_member = FamilyMember.objects.get(user=user)
            user= family_member.parent_user

        except FamilyMember.DoesNotExist:
            return user #this is the main user

@csrf_protect
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_family_members(request, member_id):
    try:
        # Get the family member by ID and make sure it belongs to the logged-in user
        family_member = FamilyMember.objects.get(uuid=member_id)
        family_user  =  family_member.user
        # family_user =  family_member.user
        # user_profile =  UserProfile.objects.get(user=family_user)
        # family_user.delete()
        # family_member.delete()
        # user_profile.delete()
        # return Response({'message': f"Deleted the family member with id {member_id}"}, status=status.HTTP_200_OK)

        logged_in_user  =  recursively_find_the_main_user(request.user)
        member_root_user=  recursively_find_the_main_user(family_member.parent_user)

        if logged_in_user  !=  member_root_user:
            return Response({'message':'You dont have permission to delete the user'},status=status.HTTP_403_FORBIDDEN)
        
        children  =  FamilyMember.objects.filter(parent_user=family_user)
        for child in children:
            child.parent_user =  logged_in_user
            child.save()
        
        UserProfile.objects.filter(user=family_user).delete()
        family_member.delete()
        family_user.delete()
        return Response({'message': f"Deleted the family member with ID {member_id}"},
                        status=status.HTTP_200_OK)
    except FamilyMember.DoesNotExist:
        return Response(
            {'message': f"Family member with ID {member_id} not found or unauthorized."},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
