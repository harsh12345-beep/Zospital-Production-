from rest_framework.decorators import api_view
from .serializers import PDFDataSerializer
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
import os
from django.shortcuts import render
from .serializers import PDFDataSerializer
from pyhtml2pdf import converter
from django.conf import settings
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import storage
from django.conf import settings
from datetime import datetime
import pytz

GOOGLE_APPLICATION_CREDENTIALS = '/app/credentials.json'
# Create a Google Cloud Storage client
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS
)
storage_client = storage.Client(credentials=credentials)
GOOGLE_CLOUD_STORAGE_BUCKET = 'patient_prescription'

def upload_to_gcs(pdf_file_path, destination_blob_name, patient_id):

    # Get the bucket
    bucket = storage_client.bucket(GOOGLE_CLOUD_STORAGE_BUCKET)

    # Create a blob and upload the file content
    blob = bucket.blob(f"{patient_id}/{destination_blob_name}")
    blob.upload_from_filename(pdf_file_path)

    # Make the blob publicly accessible
    blob.make_public()
    print("uploaded")
    return blob.public_url

def pdf_form(request):
    return render(request, 'api/form.html')

def pdfview(request):
    return render(request, 'api/pdf_template.html')
# Function to get Google Drive service


@api_view(['POST'])
def create_pdf_api(request):
    serializer = PDFDataSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        patient_id = data.get('patient_id', 'patient')

        try:
            # Render the HTML template
            html_string = render_to_string('api/pdf_template.html', data)
        except Exception as e:
            return JsonResponse({'error': f'Error rendering template: {e}'}, status=500)

        try:
            # Parse the HTML and replace static file paths
            soup = BeautifulSoup(html_string, 'html.parser')
            for img in soup.find_all('img'):
                if img.attrs.get('src', '').startswith('/static/'):
                    img['src'] = './static/' + img['src'].split('/static/')[1]
            for div in soup.find_all('div'):
                style = div.attrs.get('style', '')
                if 'background-image' in style:
                    start_index = style.find('url(') + 4
                    end_index = style.find(')', start_index)
                    static_path = style[start_index:end_index].strip("'\"")
                    if static_path.startswith('/static/'):
                        new_path = './static/' + static_path.split('/static/')[1]
                        div['style'] = style[:start_index] + new_path + style[end_index:]

            # Write to temporary HTML file
            html_string = str(soup)
            html_file_path = os.path.join(settings.BASE_DIR, 'temp.html')
            with open(html_file_path, 'w') as html_file:
                html_file.write(html_string)
        except Exception as e:
            return JsonResponse({'error': f'Error processing HTML: {e}'}, status=500)

        try:
            # Ensure the PDFs directory exists
            pdf_dir = os.path.join(settings.BASE_DIR, 'pdfs')
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
            # Get current time in India timezone
            india_tz = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(india_tz).strftime('%Y-%m-%d-%H:%M:%S')

            # Convert HTML to PDF using pyhtml2pdf
            pdf_filename = f"{current_time}{patient_id.replace(' ', '')}_report.pdf"
            pdf_file_path = os.path.join(pdf_dir, pdf_filename)
            converter.convert(f'file:///{html_file_path}', pdf_file_path)
        except Exception as e:
            return JsonResponse({'error': f'Error converting to PDF: {e}'}, status=500)

        try:
            if os.path.exists(pdf_file_path):
                gcs_url = upload_to_gcs(pdf_file_path, pdf_filename, patient_id)
                return JsonResponse({'url': gcs_url})
            else:
                return JsonResponse({'error': 'File not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error uploading to GCS: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid data', 'details': serializer.errors}, status=400)