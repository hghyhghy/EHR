
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from  ..models  import  Category
from rest_framework.response import  Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



@api_view(['GET'])
def get_category_name(request):
    categories =  Category.objects.all()
    data =[{'id':cat.id, 'name':cat.category_name} for cat in  categories]
    return Response(data)