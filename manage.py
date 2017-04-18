#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        os.environ.pop("DJANGO_SETTINGS_MODULE")
    except Exception:
        pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")

    from django.core.management import execute_from_command_line
    
    #from useful_inkleby.useful_django.views import AppUrl
    #AppUrl('vote.views').patterns()

    execute_from_command_line(sys.argv)
