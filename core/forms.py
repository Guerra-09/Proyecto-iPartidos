from django import forms


class ContactForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    message = forms.CharField(widget=forms.Textarea, label='Message')
    email = forms.EmailField(label='Email', required=False) 
