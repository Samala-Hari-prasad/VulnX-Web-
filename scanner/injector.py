from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .analyzer import analyze_response
from dashboard.models import Vulnerability

class Injector:
    def __init__(self, requester):
        self.requester = requester
        self.sqli_payloads = ["' OR 1=1 --", "' or \"a\"=\"a", "1' OR '1'='1"]
        self.xss_payloads = ["<script>alert(1)</script>", "\"><script>alert(1)</script>"]

    def inject_url(self, scan_obj, url):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            return
            
        for param in params.keys():
            # Test SQLi
            for payload in self.sqli_payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = urlunparse(parsed._replace(query=test_query))
                
                scan_obj.requests_sent += 1
                scan_obj.save()
                
                response = self.requester.get(test_url)
                if analyze_response(response, payload, 'SQLi'):
                    self._report_vuln(scan_obj, 'SQLi', url, param, payload, 'HIGH')
                    break # Stop testing this param for SQLi if found
                    
            # Test XSS
            for payload in self.xss_payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = urlunparse(parsed._replace(query=test_query))
                
                scan_obj.requests_sent += 1
                scan_obj.save()
                
                response = self.requester.get(test_url)
                if analyze_response(response, payload, 'XSS'):
                    self._report_vuln(scan_obj, 'XSS', url, param, payload, 'MEDIUM')
                    break

    def inject_form(self, scan_obj, form):
        url = form['url']
        method = form['method']
        inputs = form['inputs']
        
        if not inputs:
            return
            
        for param in inputs:
            # Test SQLi
            for payload in self.sqli_payloads:
                data = {i: "test" for i in inputs}
                data[param] = payload
                
                scan_obj.requests_sent += 1
                scan_obj.save()
                
                response = self.requester.post(url, data=data) if method == 'post' else self.requester.get(url, params=data)
                if analyze_response(response, payload, 'SQLi'):
                    self._report_vuln(scan_obj, 'SQLi', url, param, payload, 'HIGH')
                    break
                    
            # Test XSS
            for payload in self.xss_payloads:
                data = {i: "test" for i in inputs}
                data[param] = payload
                
                scan_obj.requests_sent += 1
                scan_obj.save()
                
                response = self.requester.post(url, data=data) if method == 'post' else self.requester.get(url, params=data)
                if analyze_response(response, payload, 'XSS'):
                    self._report_vuln(scan_obj, 'XSS', url, param, payload, 'MEDIUM')
                    break

    def _report_vuln(self, scan_obj, v_type, url, param, payload, severity):
        # Prevent duplicates
        if not Vulnerability.objects.filter(scan=scan_obj, type=v_type, url=url, parameter=param).exists():
            Vulnerability.objects.create(
                scan=scan_obj,
                type=v_type,
                url=url,
                parameter=param,
                payload=payload,
                severity=severity
            )
