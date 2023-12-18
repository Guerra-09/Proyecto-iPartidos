from django import forms


class ContactForm(forms.Form):
    title = forms.CharField(max_length=100, label='Titulo')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')
    email = forms.EmailField(label='Correo electronico', required=False) 
