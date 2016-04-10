
from tools.django_tools import  BakeView
from django import forms
import datetime
from models import Election, Council, Postcode
from django.forms.extras.widgets import SelectDateWidget
from amend_pdf import create_pdf

from jsignature.forms import JSignatureField
from jsignature.utils import draw_signature
from jsignature.widgets import JSignatureWidget

LocalBake = BakeView.local()


valid_elections = Election.valid_elections()

election_choices = ()

if len(valid_elections) > 1:
    election_choices += ((-1,"May Elections And EU Referendum"),)

for e in valid_elections:
    election_choices += ((e.id, e.name),)

election_choices += ( (0,"All Future Elections"),)



years = range(1900,2001)[::-1] #2001 minus 16 years + 1 for scotland

year_widget = SelectDateWidget(years=years)


class ElectionForm(forms.Form):

    election = forms.ChoiceField(label="Which Election(s) do you need a postal vote for?", choices=election_choices)
    first_names = forms.CharField(label="First names (in full)")
    surname = forms.CharField(label = "Last Name")
    dob = forms.DateField(label="Date of Birth",widget=year_widget)
    email = forms.CharField(
        label="Email address")
    phone = forms.CharField(required=False,
        label="Daytime telephone or mobile number (optional)")
    
    def clean(self):
        super(ElectionForm, self).clean()
        cd = self.cleaned_data
        election_value = cd.get('election')
        cd['universal'],cd['single_day'],cd['time_range'] = Election.get_time(election_value)


class AddressForm(forms.Form):
    add_1 = forms.CharField(label="First line of address")
    add_2 = forms.CharField(label="Second line of address (optional)",required=False)
    city = forms.CharField(label="City/Town")
    county = forms.CharField(required=False)
    postcode = forms.CharField()
    
    
    def clean(self):
        super(AddressForm,self).clean()
        cd = self.cleaned_data
        postcode = cd.get('postcode')
        if postcode:
            cd['council'] = Council.from_postcode(postcode)


class AltAddressForm(forms.Form):
    alt_add_1 = forms.CharField(label="First line of destination address", required=False)
    alt_add_2 = forms.CharField(label="Second line of destination address", required=False)
    alt_postcode = forms.CharField(label="Postcode of destination address", required=False)
    reason = forms.CharField(label = "Why do you want the ballot sent \
                            to this address instead of your registered \
                            address?", required=False)
    

    def clean(self):
        super(AltAddressForm, self).clean()
        
        add_1 = self.cleaned_data.get("alt_add_1")
        alt_postcode = self.cleaned_data.get("alt_postcode")
        reason = self.cleaned_data.get("reason")
        
        if add_1:
            if not alt_postcode or not reason:
                raise forms.ValidationError("If using an alternate address you need to include a postcode and a reason")


class ComboForm(AltAddressForm,ElectionForm, AddressForm):
    pass

class SignatureForm(forms.Form):
    signature = JSignatureField(widget=JSignatureWidget(jsignature_attrs={'width':"270px",'height':"120px"}))

"""
                signature = sig.cleaned_data.get('signature')
                if signature:
                    sig_picture = draw_signature(signature)
"""


class HomeView(LocalBake):
    """
    front page view
    """
    template = "home.html"
    url_pattern = r'^'
    url_pattern_name = "home_view"

    def view(self,request):
        
        if request.POST:
            form = ComboForm(request.POST)
            if form.is_valid():
                return create_pdf(form)
            else:
                #re run component parts to give seperate error messages
                e_form = ElectionForm(request.POST)
                add_form = AddressForm(request.POST)
                alt_form = AltAddressForm(request.POST)
                
                e_form.is_valid()
                add_form.is_valid()
                alt_form.is_valid()         
        else:
            e_form = ElectionForm()
            add_form = AddressForm()
            alt_form = AltAddressForm()
        
        return {'e_form':e_form,
                'add_form':add_form,
                'alt_form':alt_form
                }
