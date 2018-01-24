#importing forms
from django import forms 
import datetime

#creating our forms
class SignupForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field details
	page = forms.CharField(label='URL', max_length=150)
	current_year = datetime.datetime.today().year

	start_date = forms.DateField(label = 'Enter start date', widget=forms.SelectDateWidget(years=[y for y in range(2004,current_year+1)]))
	end_date = forms.DateField(label='Enter end date', initial=datetime.date.today,
								 widget=forms.SelectDateWidget(years=[y for y in range(2004,current_year+1)]))
