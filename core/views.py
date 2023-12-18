from django.shortcuts import render
from .models import FrequentlyAskedQuestions
from registration.models import Tenant
from .forms import ContactForm
from django import forms
from django.core.mail import send_mail


# Create your views here.
def home(request):

    # Esto permite que si es que el cliente no ingreso alguno de los datos no se muestre...
    clubs = Tenant.objects.exclude(clubName='')\
        .exclude(clubDescription='')\
        .exclude(clubPhoto=None)\
        .exclude(clubAddress='')\
        .exclude(clubApertureTime=None)\
        .exclude(clubClosureTime=None)\
        .order_by('-date_joined')[:3]
    return render(request, 'core/home.html', {'clubs': clubs})

def help(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email'] if not request.user.is_authenticated else request.user.email
            account_type = 'Client' if request.user.is_authenticated and request.user.role == 'client' else 'Tenant'
            message += f"\n\nEmail: {email}\nAccount Type: {account_type}"

            send_mail(
                title,
                message,
                'djangoa353@gmail.com',
                ['djangoa353@gmail.com'],
                fail_silently=False,
            )

            form = ContactForm()

    else:
        form = ContactForm()
        if request.user.is_authenticated:
            del form.fields['email']

    faqs = FrequentlyAskedQuestions.objects.all()

    return render(request, 'core/help.html', {'faqs': faqs, 'form': form})




    faqs = FrequentlyAskedQuestions.objects.all()

    return render(request, 'core/help.html', {'faqs': faqs, 'form': form})