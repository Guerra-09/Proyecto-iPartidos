from django import forms

class PaymentForm(forms.Form):
    cardName = forms.CharField(label='Nombre del titular', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cardNumber = forms.CharField( label='Número de la tarjeta', max_length=19, widget=forms.TextInput(attrs={'class': 'form-control', 'data-inputmask': "'mask': '9999 9999 9999 9999'", 'pattern': '(\d{4} ){3}\d{4}' }))
   
    cardExpiry = forms.CharField(
        label='Fecha de vencimiento (MM/AA)',
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'data-inputmask': "'mask': '99/99'",
            'pattern': '(0[1-9]|1[0-2])\/\d{2}' 
        }),
    )
    cardCVV = forms.CharField(label='CVV', max_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{3}'}))


