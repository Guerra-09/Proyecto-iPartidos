from django import forms

class PaymentForm(forms.Form):
    cardName = forms.CharField(label='Nombre del titular', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cardNumber = forms.CharField(label='Número de la tarjeta', max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{16}'}))
    cardExpiry = forms.DateField(
    label='Fecha de vencimiento (MM/AA)',
    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    cardCVV = forms.CharField(label='CVV', max_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{3}'}))