

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from ..models import FamilyMember
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_family_members(request,member_id):
    try:
        family_member = FamilyMember.objects.get(id=member_id,parent_user=request.user)
        family_user =  family_member.user

        family_user.delete()
        family_member.delete()

        return Response({'message':f"Delete the family member of id {member_id}"},status=status.HTTP_200_OK)

    except FamilyMember.DoesNotExist:
        return  Response({'message':f"Family member does not exist with {member_id} id "},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

