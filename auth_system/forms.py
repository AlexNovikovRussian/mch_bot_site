from django import forms

class MosRuForm (forms.Form):
    mosLogin = forms.CharField(max_length=100, label="Enter your Mos.Ru login", )
    mosPassword = forms.CharField(max_length=100, label="Enter your Mos.Ru password")