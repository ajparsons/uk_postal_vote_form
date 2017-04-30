# uk_postal_vote_form

Code for http://postalvote.inkleby.com/

Using OS Code Point Open + Democracy Club list of council ERO's this creates a form that makes a printable PDF of a postal vote application form. 

Tested on Django 1.8.5 and 1.11. Python 2/3 compatible.

To set up:

1. Create a proj/config.py from proj/sampleconfig.py
2. pip install -r requirements.txt
3. manage.py migrate
4. manage.py populate postalvote

And run!
