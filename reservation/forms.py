from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

class PaymentForm(forms.Form):
    cardName = forms.CharField(label='Nombre del titular', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cardNumber = forms.CharField(label='Número de la tarjeta', max_length=19, widget=forms.TextInput(attrs={'class': 'form-control', 'data-inputmask': "'mask': '9999 9999 9999 9999'"}))
    cardExpiry = forms.CharField(
        label='Fecha de vencimiento (MM/AA)',
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'data-inputmask': "'mask': '99/99'"}),
    )
    cardCVV = forms.CharField(label='CVV', max_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{3}'}))

    def clean(self):
        cleaned_data = super().clean()

        cardName = cleaned_data.get('cardName')
        cardNumber = cleaned_data.get('cardNumber')
        cardExpiry = cleaned_data.get('cardExpiry')
        cardCVV = cleaned_data.get('cardCVV')

        if not cardName or cardName.isnumeric():
            raise ValidationError('El nombre del titular no puede estar vacío.')

        if len(cardNumber.replace(' ', '')) != 16:
            raise ValidationError('El número de la tarjeta debe tener 16 dígitos.')

        if cardExpiry:
            month, year = cardExpiry.split('/')
            month = int(month)
            year = int('20' + year)
            if not (1 <= month <= 12):
                raise ValidationError('El mes de vencimiento debe estar entre 1 y 12.')
            if not (2023 <= year <= 2035):
                raise ValidationError('El año de vencimiento debe estar entre 2023 y 2035.')
        else:
            raise ValidationError('La fecha de vencimiento no puede estar vacía.')

        if not cardCVV:
            raise ValidationError('El CVV no puede estar vacío.')

        return cleaned_data