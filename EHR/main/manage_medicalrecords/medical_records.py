# Add this to your views.py for better debugging and error handling

from ..models import FamilyMember, UserProfile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from ..forms import MedicalRecordForm
from ..models import *
from rest_framework import status
import mimetypes
import logging

# Set up logging
logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = ['application/pdf', 'image/jpeg', 'image/png']

def is_valid_file(file):
    mime_type, _ = mimetypes.guess_type(file.name)
    return mime_type in ALLOWED_MIME_TYPES

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_medical_records(request, member_id):
    try:
        logger.info(f"Received POST request for member_id: {member_id}")
        logger.info(f"User: {request.user}")
        logger.info(f"POST data keys: {list(request.POST.keys())}")
        logger.info(f"FILES data keys: {list(request.FILES.keys())}")
        
        # Try to get the family member
        try:
            family_member = get_object_or_404(FamilyMember, user_id=member_id)
            logger.info(f"Found family member: {family_member}")
        except Exception as e:
            logger.error(f"Family member not found: {e}")
            return Response({
                'error': 'Family member not found or access denied'
            }, status=status.HTTP_404_NOT_FOUND)

        # Validate uploaded files' MIME types
        for file_field in ['report_file', 'prescription_file']:
            uploaded_file = request.FILES.get(file_field)
            if uploaded_file:
                logger.info(f"File {file_field}: {uploaded_file.name}, size: {uploaded_file.size}")
                if not is_valid_file(uploaded_file):
                    return Response({
                        'error': f'Invalid file type for {file_field}. Only PDF, JPG, and PNG are allowed.'
                    }, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with form processing
        form = MedicalRecordForm(request.POST, request.FILES)
        
        if form.is_valid():
            logger.info("Form is valid, saving record")
            record = form.save(commit=False)
            record.user = family_member.user
            record.save()  # The medical_category will be automatically handled by the form
            logger.info(f"Record saved with ID: {record.id}")
            return Response({
                'message': 'Record added successfully',
                'record_id': record.id
            }, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Form validation errors: {form.errors}")
            return Response({
                'error': 'Form validation failed',
                'details': form.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Unexpected error in add_medical_records: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_records(request, member_id):
    try:
        logger.info(f"Fetching records for member_id: {member_id}")
        
        # Get category parameter once at the beginning
        category = request.GET.get('category')
        logger.info(f"Category filter: {category}")
        
        # Check if using FamilyMember relationship
        try:
            family_member = get_object_or_404(FamilyMember, id=member_id, user=request.user)
            records = MedicalRecord.objects.filter(user=family_member.user).order_by('-uploaded_on')
        except:
            # Fallback to direct user_id filtering (less secure)
            logger.warning("Using direct user_id filtering - consider security implications")
            records = MedicalRecord.objects.filter(user=member_id).order_by('-uploaded_on')
        
        # Apply category filter to records (regardless of which path above was taken)
        if category and category.lower() != 'all':
            # Filter by category_name field in the Category model
            records = records.filter(medical_category__category_name__iexact=category)
            logger.info(f"Applied category filter: {category}")
            
        records_data = []
        for record in records:
            records_data.append({
                'id': record.id,
                'report_file': record.report_file.url if record.report_file else None,
                'prescription_file': record.prescription_file.url if record.prescription_file else None,
                'medicines_name': record.medicines_name,
                'prescribed_tests': record.prescribed_tests,
                'uploaded_on': record.uploaded_on.isoformat(),
                'category': record.medical_category.category_name if record.medical_category else 'Uncategorized',
                'category_id': record.medical_category.id if record.medical_category else None
            })

        logger.info(f"Found {len(records_data)} records after filtering")
        return Response({'records': records_data}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error fetching records: {str(e)}")
        return Response({'error': 'Failed to fetch records'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API endpoint to get all categories
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    try:
        categories = Category.objects.all().values('id', 'category_name')
        return Response(list(categories), status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        return Response({'error': 'Failed to fetch categories'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_medical_records(request, record_id):
#     try:
#         logger.info(f"Deleting record with ID: {record_id}")
#         record = get_object_or_404(MedicalRecord, id=record_id,user=request.user)
#         logger.info(f"Record {record_id} owned by user {record.user}, current user is {request.user}")

#         record.delete()
#         logger.info(f"Record {record_id} deleted successfully")
#         return Response({'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error deleting record: {str(e)}")
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)