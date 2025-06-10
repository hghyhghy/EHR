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
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google import genai


# Load environment variables from your .env file
load_dotenv()
# --- Configuration for Gemini API ---
client = None # Initialize client as None

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

def check_gemini_key():
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        # Initialize the new genai client globally or as needed
        client = genai.Client(api_key=api_key)
        print("Found client")
        return client
    except ValueError as e:
        print(f"Error configuring Gemini API: {e}")
        # In a production environment, you might want to log this error
        # and ensure your application handles the absence of the API key gracefully.   
@csrf_exempt # REMEMBER to handle CSRF properly in production!
def generate_report(request):
    """
    Receives aggregated record data, sends it to Gemini for a comprehensive summary,
    and returns the generated report.
    """
    client = check_gemini_key()
    if request.method == 'POST':
        try:
            if client is None:
                return JsonResponse({'error': 'Gemini API not configured. Check API key.'}, status=500)

            data = json.loads(request.body)
            # Expecting the aggregated text under the key 'allRecordsText'
            all_records_text = data.get('allRecordsText', '')

            if not all_records_text.strip():
                return JsonResponse({'error': 'No record data provided for comprehensive report generation.'}, status=400)

            model_name = 'gemini-1.5-flash' # Good for speed; consider 'gemini-1.5-pro' for more detailed analysis

            # --- CRITICAL: Crafting the Prompt for Comprehensive Summary ---
            prompt = f"""
            Please generate a comprehensive summary report in based on the following collection of patient records.
            Each record provides details about medicines, prescribed tests, and potentially other information.
            The report should synthesize information across all records, identifying commonalities, trends, and key insights. 
            
            The report format should be:
            1.  **Report Title:** A concise and relevant title (e.g., "Overview of Patient Health Records").
            2.  **Introduction:** A brief introduction to the purpose of this summary and the data source.
            3.  **Key Findings & Analysis:**
                * Summarize common medicines prescribed across records.
                * Identify frequently prescribed tests.
                * Note any recurring health issues or patterns inferred from the records (e.g., common complaints).
                * Highlight any significant individual cases or unique observations if they stand out.
            4.  **Overall Conclusion/Summary:** A concluding paragraph summarizing the key takeaways from the analysis of all records.

            Here is the data for summarization:
            ---
            {all_records_text}
            ---
            """

            # Call the Gemini API
            result = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            summarized_report = result.text
            report = generate_simple_pdf_view(summarized_report)
            return report

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return JsonResponse({'error': f'An error occurred during report generation: {e}'}, status=500)
    else:
        return
# myapp/views.py
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# def generate_simple_pdf_view(report_data_text):
#     """
#     Generates a PDF response with the provided medical record summary.
#     """
#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     story = [] # This list will hold all our content for the PDF
  
#     sections = report_data_text.strip().split('\n\n')
#     for section in sections:
#         # Check if the section starts with a numbered heading (e.g., "1. Report Title:")
#         if section.strip().startswith(('1.', '2.', '3.', '4.')):
#             lines = section.strip().split('\n')
#             first_line = lines[0]

#             # Extract the heading text (e.g., "Report Title", "Introduction")
#             # This handles cases like "1. Report Title:" and "3. Key Findings & Analysis:"
#             if ':' in first_line:
#                 heading_label = first_line.split(':', 1)[0].strip() # e.g., "1. Report Title"
#                 heading_content = first_line.split(':', 1)[1].strip() # e.g., "Summary of Patient Medical Records"
#             else:
#                 heading_label = first_line.strip() # e.g., "2. Introduction"
#                 heading_content = "" # No content after label

#             # Determine the style based on the heading number
#             if heading_label.startswith('1.'):
#                 story.append(Paragraph(f"<b><u>{heading_content}</u></b>", styles['H1']))
#                 story.append(Spacer(1, 0.2 * inch))
#             elif heading_label.startswith(('2.', '4.')):
#                 story.append(Paragraph(f"<b>{heading_content}</b>", styles['H2']))
#                 story.append(Spacer(1, 0.15 * inch))
#             elif heading_label.startswith('3.'):
#                 story.append(Paragraph(f"<b>{heading_content}</b>", styles['H2']))
#                 story.append(Spacer(1, 0.15 * inch))

#             # Add the rest of the lines as paragraphs or bullet points
#             content_lines = lines[1:]
#             for line in content_lines:
#                 if line.strip().startswith('*'):
#                     # Handle bullet points
#                     # The bullet_style ensures proper indentation
#                     story.append(Paragraph(line.strip().lstrip('* ').strip(), styles[""]))
#                 elif line.strip(): # Avoid adding empty paragraphs
#                     story.append(Paragraph(line.strip(), styles['Normal']))
#             story.append(Spacer(1, 0.2 * inch)) # Add space after each main section

#     # --- Build the PDF ---
#     doc.build(story)

#     # Get the value of the BytesIO buffer and make sure it's at the beginning.
#     pdf_value = buffer.getvalue()
#     buffer.close()

#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(pdf_value, content_type='application/pdf')
#     # Use 'inline' to display in browser (new tab), 'attachment' to force download
#     response['Content-Disposition'] = 'inline; filename="Patient_Medical_Summary.pdf"'

#     return response


########################################################
def generate_simple_pdf_view(report_data_text):
    """
    Generates a PDF response with the provided medical record summary.
    Also saves a copy locally for debugging.
    """
    print(f"=== PDF Generation Debug ===")
    print(f"Input text length: {len(report_data_text)}")
    print(f"Input preview: {report_data_text[:200]}...")
    
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [] # This list will hold all our content for the PDF

    # Always add a title first to ensure content exists
    story.append(Paragraph("<b>Medical Records Summary Report</b>", styles['Title']))
    story.append(Spacer(1, 0.3 * inch))

    if not report_data_text or len(report_data_text.strip()) < 10:
        print("WARNING: Very short or empty input")
        story.append(Paragraph("Insufficient data for report generation.", styles['Normal']))
    else:
        sections = report_data_text.strip().split('\n\n')
        print(f"Found {len(sections)} sections")
        
        for i, section in enumerate(sections):
            print(f"Processing section {i}: {section[:100]}...")
            
            # Check if the section starts with a numbered heading (e.g., "1. Report Title:")
            if section.strip().startswith(('1.', '2.', '3.', '4.')):
                lines = section.strip().split('\n')
                first_line = lines[0]

                # Extract the heading text (e.g., "Report Title", "Introduction")
                if ':' in first_line:
                    heading_label = first_line.split(':', 1)[0].strip()
                    heading_content = first_line.split(':', 1)[1].strip()
                else:
                    heading_label = first_line.strip()
                    heading_content = ""

                # Determine the style based on the heading number
                if heading_label.startswith('1.'):
                    if heading_content:
                        story.append(Paragraph(f"<b><u>{heading_content}</u></b>", styles['Heading1']))
                    story.append(Spacer(1, 0.2 * inch))
                elif heading_label.startswith(('2.', '4.')):
                    if heading_content:
                        story.append(Paragraph(f"<b>{heading_content}</b>", styles['Heading2']))
                    story.append(Spacer(1, 0.15 * inch))
                elif heading_label.startswith('3.'):
                    if heading_content:
                        story.append(Paragraph(f"<b>{heading_content}</b>", styles['Heading2']))
                    story.append(Spacer(1, 0.15 * inch))

                # Add the rest of the lines as paragraphs or bullet points
                content_lines = lines[1:]
                for line in content_lines:
                    line_stripped = line.strip()
                    if line_stripped.startswith('*'):
                        # Handle bullet points
                        bullet_text = line_stripped.lstrip('* ').strip()
                        story.append(Paragraph(f"• {bullet_text}", styles["Normal"]))
                    elif line_stripped: # Avoid adding empty paragraphs
                        story.append(Paragraph(line_stripped, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
            else:
                # Handle non-numbered sections
                lines = section.strip().split('\n')
                for line in lines:
                    line_stripped = line.strip()
                    if line_stripped.startswith('*'):
                        bullet_text = line_stripped.lstrip('* ').strip()
                        story.append(Paragraph(f"• {bullet_text}", styles["Normal"]))
                    elif line_stripped:
                        story.append(Paragraph(line_stripped, styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

    print(f"Total story elements: {len(story)}")

    # Build the PDF
    doc.build(story)

    # Get the PDF data
    pdf_value = buffer.getvalue()
    buffer.close()
    
    print(f"Generated PDF size: {len(pdf_value)} bytes")

    # === SAVE LOCALLY FOR DEBUGGING ===
    try:
        # Create a debug directory if it doesn't exist
        debug_dir = os.path.join(settings.BASE_DIR, 'debug_pdfs')
        os.makedirs(debug_dir, exist_ok=True)
        
        # Generate filename with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"medical_report_{timestamp}.pdf"
        filepath = os.path.join(debug_dir, filename)
        
        # Save the PDF
        with open(filepath, 'wb') as f:
            f.write(pdf_value)
        
        print(f"PDF saved locally at: {filepath}")
        
    except Exception as e:
        print(f"Error saving PDF locally: {e}")

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(pdf_value, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Patient_Medical_Summary.pdf"'
    
    return response


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

