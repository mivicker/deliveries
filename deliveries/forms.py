from django import forms

class UploadFileForm(forms.Form):
	date = forms.DateField(label='Delivery Day')
	file = forms.FileField(widget=forms.FileInput(
		attrs=({'id': 'upload-csv'})))