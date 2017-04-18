# -*- coding: utf-8 -*-

'''
Populate our small database to give contact details
'''

import os, django

try:
    os.environ.pop("DJANGO_SETTINGS_MODULE")
except Exception:
    pass
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
django.setup()

from vote.models import Council, Postcode, Election
from django.contrib.auth.models import User

def populate():
    Council.populate()
    Postcode.populate()
    Election.populate()


if __name__ == "__main__":
    #print Postcode.is_multi("AL4 0QR")
    populate()