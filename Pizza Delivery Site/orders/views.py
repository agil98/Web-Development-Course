from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    context = {
        "salads" : Salad.objects.all()
    }
    return render(request, "orders/index.html", context)
