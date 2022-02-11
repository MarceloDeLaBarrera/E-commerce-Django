from email.policy import default
from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Asunto', "class": "form-control", "style": "text-align:center"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Email', "class": "form-control", "style": "text-align:center"}))
    phone_number = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Teléfono', "class": "form-control", "style": "text-align:center"}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Mensaje', "class": "form-control", "style": "text-align:center"}))
