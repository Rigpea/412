## hw/view.py
## the logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time, random

# Create your views here.

def home(request):
    ''''A function to respond to the  /hw URLF.
        This funciton will delgate work to an HTML template
    '''

    template_name = "hw/home.html"
    #create some text

    #create a dict of context variables
    context = {
        'current_time': time.ctime(), 
        'letter1' : chr(random.randint(65,90)), 
        'letter2' : chr(random.randint(65,90)), 
        'number' : random.randint(1,10),

    }

    #return a respone to the lcinet 
    return render(request, template_name, context)
