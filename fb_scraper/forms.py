#importing forms
from django import forms 
 
#creating our forms
class SignupForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field details
	page = forms.CharField(label='Enter company/page name', max_length=100)