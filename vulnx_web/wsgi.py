import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnx_web.settings')
application = get_wsgi_application()
app = application  # Required by Vercel
