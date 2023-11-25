# lighthouse_app/views.py
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import ScanResult
import subprocess
import tempfile
import os
from django.db import transaction
from django.utils import timezone

class RunLighthouseScanView(View):
    template_name = 'scan_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.POST.get('user')
        url = request.POST.get('url')
        device = request.POST.get('device', 'desktop')  # Default to desktop if not provided

        try:
            with transaction.atomic():
                temp_filename = self.run_lighthouse_scan(url, user, device)

                # Save scan result to the database
                scan_result = ScanResult.objects.create(user=user, url=url, report=self.read_file(temp_filename))

                # Remove the temporary file
                os.remove(temp_filename)

            # Render the JSON content within the view
            return HttpResponse(scan_result.report, content_type='application/json')

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            error_message = f"Error occurred during the Lighthouse scan: {str(e)}"
            return HttpResponse(error_message, status=500, content_type='text/plain')

    def run_lighthouse_scan(self, url, user, device):
        # Sanitize the URL to create a valid filename
        sanitized_url = ''.join(c if c.isalnum() else '_' for c in url)
        
        # Create a temporary file with a unique name
        temp_filename = f"lighthouse_{user}_{sanitized_url}_{device}_{timezone.now().strftime('%Y%m%d%H%M%S%f')}.json"

        try:
            # Run Lighthouse command and save the report to the temporary file
            lighthouse_command = f"lighthouse {url} --output-path {temp_filename} --chrome-flags='--headless' --emulated-form-factor={device}"
            subprocess.run(lighthouse_command, shell=True, check=True)

            return temp_filename

        except subprocess.CalledProcessError as e:
            # Handle subprocess errors
            raise Exception(f"Lighthouse process returned non-zero exit code: {e.returncode}")

    def read_file(self, filename):
        try:
            # Read the content from the file
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            return content

        except FileNotFoundError:
            # Handle file not found error
            raise Exception(f"File not found: {filename}")

        except Exception as e:
            # Handle other file operation errors
            raise Exception(f"Error reading file: {str(e)}")
        
class ScanResultListView(View):
    template_name = 'scan_result_list.html'

    def get(self, request):
        results = ScanResult.objects.order_by('-id')  # Order by descending id
        return render(request, self.template_name, {'results': results})


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

class DownloadScanReportView(View):
    def get(self, request, result_id, format):
        result = ScanResult.objects.get(id=result_id)
        content_type = 'text/html' if format == 'html' else 'application/json' if format == 'json' else 'application/pdf'

        if format == 'pdf':
            report_content = render_to_string('pdf_report_template.html', {'result': result})
            pdf_file = HTML(string=report_content).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{result.url}_report.pdf"'
        else:
            report_content = result.report
            response = HttpResponse(report_content, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{result.url}_report.{format}"'

        return response


import csv

class ExportScanDataView(View):
    def get(self, request):
        results = ScanResult.objects.all()
        csv_content = self.generate_csv(results)

        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="scan_data.csv"'

        return response

    def generate_csv(self, results):
        fields = ['user', 'url', 'report']
        csv_content = []

        # Write the header
        csv_content.append(','.join(fields))

        # Write the data rows
        for result in results:
            row = [getattr(result, field) for field in fields]
            csv_content.append(','.join(map(str, row)))

        return '\n'.join(csv_content)
