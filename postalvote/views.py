
from .forms import ComboForm, ElectionForm, AddressForm, AltAddressForm
from .amend_pdf import create_pdf
from django.shortcuts import render
from django.template import RequestContext
def postal_vote_form_view(request):

	if request.POST:
		form = ComboForm(request.POST)
		if form.is_valid():
			return create_pdf(form) #return pdf object
		else:
			# re run component parts to return separate error messages
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

	context = {'e_form': e_form,
					'add_form': add_form,
					'alt_form': alt_form
					}

	return render(request,"home.html", context)
