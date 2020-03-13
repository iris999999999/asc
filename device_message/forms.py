from django import forms

class DateForm(forms.Form):
	date_1 = forms.CharField(label='дата с')
	date_2 = forms.CharField(label='по')
	

class Organization_Form(forms.Form):
	organization_list = forms.ChoiceField(label='предприятие')
