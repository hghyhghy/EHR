

from rest_framework.response  import  Response
from rest_framework.decorators  import  api_view,permission_classes
from  rest_framework.permissions import  IsAuthenticated
from django.shortcuts import render, get_object_or_404
from  forms  import  MedicalRecordForm
from  ..models import  MedicalRecord
from rest_framework  import  status

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def medical_records_view(request):
    if request.method == 'POST':
        form   =  MedicalRecordForm(request.POST,request.FILES)

        if form.is_valid():
            record =  form.save(commit=False)
            record.user =  request.user
            record.save()
            return  Response({'message':'Records updated successfully'},status=status.HTTP_200_OK)

        else:
            return  Response({'error':form.error},status=status.HTTP_403_FORBIDDEN)

    #rendering template normally for get  

    form  =  MedicalRecordForm()
    records =  MedicalRecord.objects.filter(user=request.user).order_by('-uploade_on')
    return render(request, 'main/medical_records.html', {'form': form, 'records': records})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_records(request,record_id):
    record  =  get_object_or_404(MedicalRecord,id=record_id, user=request.user)
    record.delete()
    return Response({'message': 'Record deleted successfully'}, status=200)
