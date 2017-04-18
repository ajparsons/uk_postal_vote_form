"""
WSGI config for generic inkleby project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
sys.path.append("..\\inkleby_django\\")
sys.path.append("../../useful_inkleby")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
