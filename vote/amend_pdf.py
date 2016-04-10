from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import datetime
import os
from django.http import HttpResponse
from django.conf import settings

def write_date(draw,x,y,date,increment=14,extra_spacing=[]):
    date_format = date.strftime("%d%m%Y")
    for i,d in enumerate(date_format):
        draw(x,y,d)
        x += increment
        if i in extra_spacing:
            x+= 18


def file_name_safe(filename):
    keepcharacters = (' ','.','_')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
    
def create_front_page(council,postcode):
    """
    information page
    """
    body = []
    ba = body.append
    
    ba("Postal Vote Application")
    ba("")
    
    if council:
        
        address = council.address.split("\n")
        naddress = ["Electoral Registration Officer"]
        for a in address:#removes duplicates from formatting
            a = a.strip()
            if a not in naddress:
                naddress.append(a)
                
        naddress.append(council.postcode)
        
        
        ba("From your postcode ({0}) we think you live in:".format(postcode))
           
        ba(council.name)
        ba("")
        ba("If this is right - you need to sign the form on the next page and send it to:")
        
        ba("")
        for a in naddress:
            ba(a)
        ba("")
        if council.phone:
            ba("Phone: {0}".format(council.phone))
            
            
    else:
        ba("We can't find the council for your postcode - is this postcode correct? {0}".format(postcode))
           
        ba("Visit aboutmyvote.co.uk to find the address for your local Electoral Registration Officer")

        
    ba("")
    ba("For the Electoral Commission page on postal voting \
        visit www.aboutmyvote.co.uk ")
    ba("")
    ba("This form was pre-populated at postalvote.inkleby.com")
    
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab

    can = canvas.Canvas(packet)
    
    x = 700
    for r in body:
        can.drawString(40, x, r)
        x -= 15
        
    can.save()
    
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    return new_pdf.getPage(0)

def create_pdf(form=None,sig_image=None):
    """
    creates an overlap to add text to the original pdf
    """
    
    def get_from_form(value):
        if form:
            return form.cleaned_data.get(value,"")
        else:
            return ""
    
    email = get_from_form("email")
    phone_number = get_from_form("phone")
    postcode = get_from_form("postcode")
    surname = get_from_form("surname")
    firstnames = get_from_form("first_names")
    add1 = get_from_form("add_1")
    add2 = get_from_form("add_2")
    city = get_from_form("city")
    county = get_from_form("county")
    alt_add1 = get_from_form("alt_add_1")
    alt_add2 = get_from_form("alt_add_2")
    alt_postcode = get_from_form("alt_postcode")
    alt_reason = get_from_form("reason")
    
    file_name = file_name_safe("{0}_{1}".format(surname,firstnames).lower())
    
    council = get_from_form("council")
    

    if city and county:
        add3 = city + ", " + county
    elif city:
        add3 = city
    elif county:
        add3 = county

    until_further_notice = get_from_form("universal")
    one_date = get_from_form("single_day")
    date_range = get_from_form("time_range")
    date_of_birth = get_from_form("dob")

    
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab

    can = canvas.Canvas(packet, pagesize=letter)
    
    #add signature of present
    if sig_image:
        can.drawImage(ImageReader(sig_image), 293, 155, mask='auto')
    #core address info
    
    can.drawString(40, 667, surname.upper())
    can.drawString(40, 620, firstnames.upper())
    
    can.drawString(40, 561, add1.upper())
    can.drawString(40, 541, add2.upper())
    can.drawString(40, 521, add3.upper())
    
    can.drawString(40, 390, email.upper())
    can.drawString(40, 451, phone_number)
    can.drawString(100, 499, postcode.upper())
    
    
    #alt address
    
    can.drawString(285, 646, alt_add1.upper())
    can.drawString(285, 626, alt_add2.upper())
    can.drawString(350, 606, alt_postcode.upper())
    can.drawString(285, 548, alt_reason.upper())
    
    #for how long we want this on
    
    if until_further_notice:
        can.drawString(30, 278, "X")
    if one_date:
        can.drawString(30, 248, "X")
        write_date(can.drawString,153,213,one_date)
    if date_range:
        can.drawString(30, 181, "X")
        write_date(can.drawString,153,156,date_range[0])
        write_date(can.drawString,153,129,date_range[1])
    
    # today's date
    
    write_date(can.drawString,457,44,datetime.datetime.now())
    
    #birthdate
    
    can.setFont("Helvetica", 30) #choose your font type and font size
    write_date(can.drawString,310,350,date_of_birth, 25, extra_spacing=[1,3])
    
    can.save()
    
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read existing PDF
    
    front_page = create_front_page(council, postcode)
    
    source_file = os.path.join( settings.PROJECT_PATH,
                                "resources",
                                "form.pdf")
    existing_pdf = PdfFileReader(file(source_file, "rb"))
                
                                      
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(front_page)
    output.addPage(page)
    # send the stream into a response and return it to the view
    
    outputStream = StringIO.StringIO()
    output.write(outputStream)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="postal_vote_{0}.pdf"'.format(file_name)
    response.write(outputStream.getvalue())
    
    outputStream.close()
    if council:
        council.increment_count()
    return response