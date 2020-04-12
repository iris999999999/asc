from django import forms
from datetime import datetime, date, time

class DateForm(forms.Form):	
	


	date1 = forms.DateTimeField(label = 'Период c',widget = forms.TextInput(attrs = {'size': '10','left':'5px'}),initial=format(datetime.combine(date.today(),time()),'%d/%m/%Y %H:%M'), localize=True)
	date2 = forms.DateTimeField(label = 'пo',widget = forms.TextInput(attrs = {'size': '10'}),initial=format(datetime.combine(date.today(),time(23,0)),'%d/%m/%Y %H:%M'), localize=True)


class Organization_Form(forms.Form):

	CHOICES = (('1', 'Предприятие'),('2', 'РеПлас-М'),('3', 'ПРОМОПАК'))
	organization_list = forms.ChoiceField(choices=CHOICES,label = False)
	#organization_list = forms.ChoiceField(choices=CHOICES,label = 'Предприятие')
	

