from django.shortcuts import render
from .services import get_indicators

def home(request):
    indicators = get_indicators()
    return render(request, 'moneda.html', {'indicators': indicators})
