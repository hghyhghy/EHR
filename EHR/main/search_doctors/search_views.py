
from  rest_framework.response import  Response
from ..models  import  DoctorProfile
from  django.db.models import  Q
from django.views.decorators.csrf import  csrf_exempt
from  rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from  django.views.decorators.csrf import  csrf_protect


@csrf_protect
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def searh_doctors_by_category(request):

    query =  request.GET.get('category','').strip()

    if query:
        
        doctor =  DoctorProfile.objects.filter(
            category_id__category_name__icontains =  query
        )
    else:
        doctor =  DoctorProfile.objects.all()

    
    data = [{

            'username':doc.username,
            'degree':doc.degree,
            'category':doc.category_id.category_name,
            'phone_number':doc.phone_number
    } for doc in  doctor]

    return  Response(data, status=status.HTTP_200_OK)