from django.shortcuts import render

# Create your views here.
from .form import HashForm


def home(request):
    form = HashForm()
    return render(request, 'hashing/home.html', {'form': form})