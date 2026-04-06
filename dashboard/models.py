from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Scan(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scans', null=True, blank=True)
    target_url = models.URLField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    urls_scanned = models.IntegerField(default=0)
    requests_sent = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.target_url} - {self.status}"

class Vulnerability(models.Model):
    SEVERITY_CHOICES = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
        ('INFO', 'Info'),
    )
    
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='vulnerabilities')
    type = models.CharField(max_length=100) # e.g., SQLi, XSS
    url = models.URLField(max_length=1000)
    parameter = models.CharField(max_length=100, blank=True, null=True)
    payload = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='LOW')

    def __str__(self):
        return f"[{self.severity}] {self.type} at {self.url}"
