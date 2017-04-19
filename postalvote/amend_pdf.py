from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import datetime
import os
from django.http import HttpResponse
from django.conf import settings

try:
	from StringIO import BytesIO 
except ImportError:
	from io import BytesIO 


def write_date(draw, x, y, date, increment=14, extra_spacing=[]):
	date_format = date.strftime("%d%m%Y")
	for i, d in enumerate(date_format):
		draw(x, y, d)
		x += increment
		if i in extra_spacing:
			x += 18


def file_name_safe(filename):
	keepcharacters = (' ', '.', '_')
	return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


def create_front_page(council, postcode, multi_council=1):
	"""
	create information page - about service, where to send form.
	"""
	body = []
	line = body.append

	line("Postal Vote Application")
	line("")

	if council:

		address = council.address.split("\n")
		naddress = ["Electoral Registration Officer"]
		for a in address:  # removes duplicate lines from formatting
			a = a.strip()
			if a not in naddress:
				naddress.append(a)

		naddress.append(council.postcode)

		line("From your postcode ({0}) we think you live in:".format(postcode))
		line("")
		line(council.name)
		line("")

		"""
		Adds Warning for postcodes that cross multiple areas
		https://democracyclub.org.uk/blog/2017/03/20/4314-times-when-postcodes-arent-good-enough/
		"""
		if multi_council > 1:
			line("BE CAREFUL: Your postcode covers multiple councils. Please check this is correct.")
			line("")

		line("If this is right - you need to sign the form on the next page and send it to:")

		line("")
		for a in naddress:
			line(a)
		line("")
		if council.phone:
			line("Phone: {0}".format(council.phone))

	else:
		line("We can't find the council for your postcode - is this postcode correct? {0}".format(
			postcode))

		line("Visit aboutmyvote.co.uk to find the address for your local Electoral Registration Officer")

	line("")
	line("For the Electoral Commission page on postal voting visit www.aboutmyvote.co.uk")
	line("")
	line("This form was pre-populated at postalvote.inkleby.com")

	packet = BytesIO()
	# create a new PDF with Reportlab

	can = canvas.Canvas(packet)

	x = 700
	for r in body:
		can.drawString(40, x, r)
		x -= 15

	can.save()

	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	return new_pdf.getPage(0) #return a pdf page


def create_pdf(form=None, sig_image=None):
	"""
	given form results - 
	"""

	def get_from_form(value):
		if form:
			return form.cleaned_data.get(value, "")
		else:
			return ""
			
	email = get_from_form("email")
	phone_number = get_from_form("phone")
	postcode = get_from_form("postcode")
	surname = get_from_form("surname")
	first_names = get_from_form("first_names")
	add_1 = get_from_form("add_1")
	add_2 = get_from_form("add_2")
	city = get_from_form("city")
	county = get_from_form("county")
	alt_add_1 = get_from_form("alt_add_1")
	alt_add_2 = get_from_form("alt_add_2")
	alt_postcode = get_from_form("alt_postcode")
	alt_reason = get_from_form("reason")
	
	file_name = file_name_safe("{0}_{1}".format(surname, first_names).lower())

	council = get_from_form("council")
	multi_council = get_from_form("multi_council")

	if city and county:
		add_3 = city + ", " + county
	elif city:
		add_3 = city
	elif county:
		add_3 = county

	until_further_notice = get_from_form("universal")
	one_date = get_from_form("single_day")
	date_range = get_from_form("time_range")
	date_of_birth = get_from_form("dob")

	packet = BytesIO()
	# create a new PDF with Reportlab

	can = canvas.Canvas(packet, pagesize=letter)

	# add signature of present
	if sig_image:
		can.drawImage(ImageReader(sig_image), 293, 155, mask='auto')
	# core address info

	can.drawString(40, 667, surname.upper())
	can.drawString(40, 620, first_names.upper())

	can.drawString(40, 561, add_1.upper())
	can.drawString(40, 541, add_2.upper())
	can.drawString(40, 521, add_3.upper())

	can.drawString(40, 390, email.upper())
	can.drawString(40, 451, phone_number)
	can.drawString(100, 499, postcode.upper())

	# alt address

	can.drawString(285, 646, alt_add_1.upper())
	can.drawString(285, 626, alt_add_2.upper())
	can.drawString(350, 606, alt_postcode.upper())
	can.drawString(285, 548, alt_reason.upper())

	# for how long we want this on

	if until_further_notice:
		can.drawString(30, 278, "X")
	if one_date:
		can.drawString(30, 248, "X")
		write_date(can.drawString, 153, 213, one_date)
	if date_range:
		can.drawString(30, 181, "X")
		write_date(can.drawString, 153, 156, date_range[0])
		write_date(can.drawString, 153, 129, date_range[1])

	# today's date

	write_date(can.drawString, 457, 44, datetime.datetime.now())

	# birthdate

	can.setFont("Helvetica", 30)
	write_date(
		can.drawString, 310, 350, date_of_birth, 25, extra_spacing=[1, 3])

	can.save()

	packet.seek(0)
	new_pdf = PdfFileReader(packet)

	front_page = create_front_page(council, postcode, multi_council)

	source_file = os.path.join(settings.PROJECT_PATH,
							   "resources",
							   "form.pdf")
	existing_pdf = PdfFileReader(open(source_file, "rb"))

	output = PdfFileWriter()
	
	# add the several pages objects to one pdf
	
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(front_page)
	output.addPage(page)
	
	# send the stream into a response and return it to the view

	outputStream = BytesIO()
	output.write(outputStream)

	response = HttpResponse(content_type='application/pdf')
	response[
		'Content-Disposition'] = 'attachment; filename="postal_vote_{0}.pdf"'.format(file_name)
	response.write(outputStream.getvalue())

	outputStream.close()
	if council:
		council.increment_count()
	return response
