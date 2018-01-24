from django.shortcuts import render
from forms import SignupForm
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect, HttpResponse
import fb_scrap
import datetime

def signupform(request):
    #if form is submitted
    if request.method == 'POST':
        form = SignupForm(request.POST)

        #checking the form is valid or not
        if form.is_valid():
            #if valid rendering new view with values
            #the form values contains in cleaned_data dictionary
            page_name = form.cleaned_data['page'].split('/')[-1]
            start_date = form.cleaned_data['start_date']
            fb_scrap.start_date = start_date
            end_date= form.cleaned_data['end_date']
            fb_scrap.end_date = end_date
            fb_scrap.page_id = page_name.split('/')[-1]
            diff_days = ((end_date + datetime.timedelta(1)) - (start_date - datetime.timedelta(1))).days
            fb_scrap.diff_days = diff_days
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s'%page_name+'_FB_activity.csv'
            fb_scrap.do_scraping(response)
            return response
    else:
        #creating a new form
        form = SignupForm()
        #returning form
    return render(request, 'signupform.html', {'form':form})
