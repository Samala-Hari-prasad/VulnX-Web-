from rest_framework import serializers
from .models import Scan, Vulnerability

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__'

class ScanSerializer(serializers.ModelSerializer):
    vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)
    vulnerabilities_count = serializers.SerializerMethodField()

    class Meta:
        model = Scan
        fields = ['id', 'target_url', 'status', 'start_time', 'end_time', 'urls_scanned', 'requests_sent', 'vulnerabilities', 'vulnerabilities_count']

    def get_vulnerabilities_count(self, obj):
        return obj.vulnerabilities.count()
