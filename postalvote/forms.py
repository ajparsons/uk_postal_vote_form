from django import forms
from .models import Election , Postcode
from django.forms.extras.widgets import SelectDateWidget

#from jsignature.forms import JSignatureField
#from jsignature.utils import draw_signature
#from jsignature.widgets import JSignatureWid#get

valid_elections = Election.valid_elections()

election_choices = ()
"""
old code -1 is hardcoded to give the date range between these two
elections.
if len(valid_elections) > 0:
	election_choices += ((-1,"May Elections And EU Referendum"),)
"""
for e in valid_elections:
	election_choices += ((e.id, e.name),)

election_choices += ((0, "All Future Elections"),)

years = range(1900, 2003)[::-1] #allow younger people to register (For scotland)

year_widget = SelectDateWidget(years=years)

class ElectionForm(forms.Form):
	"""
	form components for basic name and election details.
	returns additional entries 'universal', 'single_day' and 'time_range'
	based on what kind of form is needed.
	"""
	election = forms.ChoiceField(
		label="Which Election(s) do you need a postal vote for?", choices=election_choices)
	first_names = forms.CharField(label="First names (in full)")
	surname = forms.CharField(label="Last Name")
	dob = forms.DateField(label="Date of Birth", widget=year_widget)
	email = forms.CharField(
		label="Email address")
	phone = forms.CharField(required=False,
							label="Daytime telephone or mobile number (optional)")

	def clean(self):
		super(ElectionForm, self).clean()
		cd = self.cleaned_data
		election_value = cd.get('election')
		cd['universal'], cd['single_day'], cd[
			'time_range'] = Election.get_time(election_value)


class AddressForm(forms.Form):
	"""
	takes postcode information and adds:
	'council' - a Council object
	'multi_council' - if the postcode is one that crosses boundaries
	"""
	add_1 = forms.CharField(label="First line of address")
	add_2 = forms.CharField(
		label="Second line of address (optional)", required=False)
	city = forms.CharField(label="City/Town")
	county = forms.CharField(required=False)
	postcode = forms.CharField()

	def clean(self):
		super(AddressForm, self).clean()
		cd = self.cleaned_data
		postcode = cd.get('postcode')
		if postcode:
			postcode_obj = Postcode.get_postcode(postcode)
			cd['multi_council'] = postcode_obj.multi_council
			cd['council'] = postcode_obj.council


class AltAddressForm(forms.Form):
	"""
	Allow user to specify an alternate place to send postal vote
	- requires region if add_1 but no reason
	"""
	alt_add_1 = forms.CharField(
		label="First line of destination address", required=False)
	alt_add_2 = forms.CharField(
		label="Second line of destination address", required=False)
	alt_postcode = forms.CharField(
		label="Postcode of destination address", required=False)
	reason = forms.CharField(label="Why do you want the ballot sent \
							to this address instead of your registered \
							address?", required=False)

	def clean(self):
		super(AltAddressForm, self).clean()

		add_1 = self.cleaned_data.get("alt_add_1")
		alt_postcode = self.cleaned_data.get("alt_postcode")
		reason = self.cleaned_data.get("reason")

		if add_1:
			if not alt_postcode or not reason:
				raise forms.ValidationError(
					"If using an alternate address you need to include a postcode and a reason")


class ComboForm(AltAddressForm, ElectionForm, AddressForm):
	pass

"""
class SignatureForm(forms.Form):
#unused scary online sig tool
	signature = JSignatureField(
		widget=JSignatureWidget(jsignature_attrs={'width': "270px", 'height': "120px"}))

	def get_image(self)
				signature = self.cleaned_data.get('signature')
				if signature:
					return draw_signature(signature)
"""