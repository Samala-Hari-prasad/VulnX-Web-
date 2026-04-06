from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, requester, base_url, max_depth=2):
        self.requester = requester
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = [(base_url, 0)]
        self.forms = []

    def crawl(self, scan_obj):
        while self.to_visit:
            current_url, depth = self.to_visit.pop(0)
            
            if current_url in self.visited or depth > self.max_depth:
                continue
                
            self.visited.add(current_url)
            
            # Update scan object
            scan_obj.urls_scanned = len(self.visited)
            scan_obj.requests_sent += 1
            scan_obj.save()
            
            response = self.requester.get(current_url)
            if not response or response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract links
            for link in soup.find_all('a', href=True):
                full_url = urljoin(current_url, link['href'])
                parsed_url = urlparse(full_url)
                
                # Stay in domain
                if parsed_url.netloc == self.domain and full_url not in self.visited:
                    self.to_visit.append((full_url, depth + 1))
                    
            # Extract forms
            for form in soup.find_all('form'):
                action = form.get('action')
                method = form.get('method', 'get').lower()
                full_action = urljoin(current_url, action) if action else current_url
                
                inputs = []
                for input_tag in form.find_all(['input', 'textarea']):
                    name = input_tag.get('name')
                    if name:
                        inputs.append(name)
                        
                self.forms.append({
                    'url': full_action,
                    'method': method,
                    'inputs': inputs
                })

        return self.visited, self.forms
