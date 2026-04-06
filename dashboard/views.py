from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Scan, Vulnerability
import threading
from scanner.engine import start_scan_engine
import json

def home(request):
    if request.method == 'POST':
        target_url = request.POST.get('target_url')
        depth = int(request.POST.get('depth', 2))
        threads = int(request.POST.get('threads', 5))
        
        user_to_save = request.user if request.user.is_authenticated else None
        
        scan = Scan.objects.create(
            user=user_to_save,
            target_url=target_url,
            status='PENDING'
        )
        
        # Start background thread
        thread = threading.Thread(target=start_scan_engine, args=(scan.id, depth, threads))
        thread.start()
        
        return redirect('dashboard:scan_live', scan_id=scan.id)
        
    scans = Scan.objects.all().order_by('-start_time')
    return render(request, 'dashboard/home.html', {'scans': scans})

def scan_live(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)
    return render(request, 'dashboard/live_scan.html', {'scan': scan})

def scan_results(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)
    vulns = scan.vulnerabilities.all()
    
    severity = request.GET.get('severity')
    vuln_type = request.GET.get('type')
    
    if severity:
        vulns = vulns.filter(severity__iexact=severity)
    if vuln_type:
        vulns = vulns.filter(type__icontains=vuln_type)
        
    return render(request, 'dashboard/results.html', {'scan': scan, 'vulnerabilities': vulns})

def api_scan_status(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)
    vulns = scan.vulnerabilities.all().values('type', 'url', 'severity', 'parameter')
    return JsonResponse({
        'status': scan.status,
        'urls_scanned': scan.urls_scanned,
        'requests_sent': scan.requests_sent,
        'vulnerabilities_count': vulns.count(),
        'recent_vulnerabilities': list(vulns)[:5]
    })

def export_report(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id)
    fmt = request.GET.get('format', 'json')
    vulns = list(scan.vulnerabilities.all().values('type', 'url', 'parameter', 'payload', 'severity'))
    
    if fmt == 'json':
        data = {
            'target_url': scan.target_url,
            'start_time': str(scan.start_time),
            'end_time': str(scan.end_time),
            'status': scan.status,
            'vulnerabilities': vulns
        }
        response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="scan_report_{scan.id}.json"'
        return response
    elif fmt == 'html':
        return render(request, 'dashboard/report.html', {'scan': scan, 'vulnerabilities': scan.vulnerabilities.all()})
    
    return HttpResponse("Invalid format")
