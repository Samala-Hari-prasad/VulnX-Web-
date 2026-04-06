import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnx_web.settings')
django.setup()

from django.contrib.auth.models import User

user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
user.set_password('admin123')
user.is_superuser = True
user.is_staff = True
user.save()

print("User admin secured with password admin123")
