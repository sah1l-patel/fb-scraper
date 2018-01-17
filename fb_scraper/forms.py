#importing forms
from django import forms 
from datetime import datetime

#creating our forms
class SignupForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field details
	page = forms.CharField(label='Enter company/page name', max_length=100)
	current_year = datetime.today().year

	start_date = forms.DateField(label = 'Enter start date', widget=forms.SelectDateWidget(years=[y for y in range(2004,current_year)]))
	end_date = forms.DateField(label='Enter end date',
								 widget=forms.SelectDateWidget(years=[y for y in range(2004,current_year)]))