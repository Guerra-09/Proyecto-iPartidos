from django.shortcuts import render

# Create your views here.
def canchaScreen(request):
    return render(request, 'canchas/look.html')