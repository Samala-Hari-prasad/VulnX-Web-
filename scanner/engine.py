import threading
from django.utils import timezone
from dashboard.models import Scan
from .requester import Requester
from .crawler import Crawler
from .injector import Injector
import concurrent.futures

def engine_worker(scan_id, depth, threads):
    try:
        scan = Scan.objects.get(id=scan_id)
        scan.status = 'RUNNING'
        scan.save()
        
        requester = Requester()
        crawler = Crawler(requester, scan.target_url, max_depth=depth)
        
        # 1. Crawl
        urls, forms = crawler.crawl(scan)
        
        # 2. Inject
        injector = Injector(requester)
        
        # Parallelize injection using ThreadPoolExecutor for URLs
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for url in urls:
                executor.submit(injector.inject_url, scan, url)
                
        # Inject forms sequentially or parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for form in forms:
                executor.submit(injector.inject_form, scan, form)
                
        # Refresh scan to get updated stats
        scan.refresh_from_db()
        scan.status = 'COMPLETED'
        scan.end_time = timezone.now()
        scan.save()
        
    except Exception as e:
        scan = Scan.objects.get(id=scan_id)
        scan.status = 'FAILED'
        scan.end_time = timezone.now()
        scan.save()
        print(f"Scan failed: {e}")

def start_scan_engine(scan_id, depth=2, threads=5):
    # This runs in a background thread triggered by the view
    engine_worker(scan_id, depth, threads)
