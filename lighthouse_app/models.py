# lighthouse_app/models.py

from django.db import models

class ScanResult(models.Model):
    user = models.CharField(max_length=255)
    url = models.URLField()
    report = models.TextField()
