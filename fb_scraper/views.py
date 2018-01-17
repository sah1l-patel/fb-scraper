from django.shortcuts import render
from forms import SignupForm
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect, HttpResponse
import fb_scrap

def signupform(request):
	#if form is submitted
	if request.method == 'POST':
		form = SignupForm(request.POST)
		 
		#checking the form is valid or not 
		if form.is_valid():
			#if valid rendering new view with values
			#the form values contains in cleaned_data dictionary
			page_name = form.cleaned_data['page']
			print page_name
			start_date = form.cleaned_data['start_date']
			print start_date
			fb_scrap.page_id = page_name
			response = HttpResponse(content_type='text/csv')
    		response['Content-Disposition'] = 'attachment; filename=%s'%page_name+'_facebook_scrap.csv'
    		fb_scrap.do_scraping(response)
    		return response
    	else:
    	#creating a new form
    		form = SignupForm()
	 
	#returning form 
	return render(request, 'signupform.html', {'form':form});