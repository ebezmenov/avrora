from django import forms

class CSVUploadForm(forms.Form):
    file_cvs=forms.FileField(label=u'CSV File')