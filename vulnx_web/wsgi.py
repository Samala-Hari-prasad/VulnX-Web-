import os
import shutil

if os.environ.get('VERCEL') == '1':
    db_path = '/tmp/db.sqlite3'
    if not os.path.exists(db_path):
        source_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
        if os.path.exists(source_db):
            shutil.copy2(source_db, db_path)

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnx_web.settings')
application = get_wsgi_application()
app = application  # Required by Vercel
