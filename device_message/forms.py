from django import forms
from datetime import datetime, date, time

class DateForm(forms.Form):	
	
	t = time(0,0) 

	date1 = forms.DateTimeField(label = 'Период c',widget = forms.TextInput(attrs = {'size': '10','left':'5px'}),initial=format(datetime.combine(date.today(),time()),'%Y/%m/%d %H:%M'), localize=True)
	date2 = forms.DateTimeField(label = 'пo',widget = forms.TextInput(attrs = {'size': '10'}),initial=format(datetime.now(),'%Y/%m/%d %H:%M'), localize=True)


class Organization_Form(forms.Form):

	CHOICES = (('1', ''),('2', 'РеПлас-М'),('3', 'ПРОМОПАК'))
	organization_list = forms.ChoiceField(choices=CHOICES,label = 'Предприятие')
	

