# lighthouse_app/urls.py

# lighthouse_app/urls.py

from django.urls import path
from .views import ScanResultListView, RunLighthouseScanView, DownloadScanReportView, ExportScanDataView

urlpatterns = [
    path('scan-results/', ScanResultListView.as_view(), name='scan-result-list-view'),
    path('run-lighthouse-scan/', RunLighthouseScanView.as_view(), name='run-lighthouse-scan-view'),
    path('download-scan-report/<int:result_id>/<str:format>/', DownloadScanReportView.as_view(), name='download-scan-report'),
    path('export-scan-data/', ExportScanDataView.as_view(), name='export-scan-data'),
]

