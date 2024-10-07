# quotes/views.py

from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.




QUOTES = [
    "The key to immortality is first living a life worth remembering.",
    "Mistakes are always forgivable, if one has the courage to admit them.",
    "If you spend too much time thinking about a thing, you'll never get it done."
]

IMAGES = [
    "https://m.media-amazon.com/images/M/MV5BMGVhNTdlNzQtYTk1OC00OTI2LTk1MDctMzBmNmU2ZDkyYzMyXkEyXkFqcGdeQXVyNjc5NjEzNA@@._V1_.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg1DDU8JeuH7oTbcNfLhd2X02xtJfWrTvY9Q&s",
    "https://cdn.legit.ng/images/1120/d34d8a10eee7570b.jpeg?v=1"
]


def quote(request):
    random_quote = random.choice(QUOTES)
    random_image = random.choice(IMAGES)
    context = {'quote': random_quote, 'image': random_image}
    return render(request, 'quotes/quote.html', context)


def show_all(request):

    quotes_images = zip(QUOTES, IMAGES)
    context = {'quotes_images': quotes_images}
    return render(request, 'quotes/show_all.html', context)


def about(request):
    context = {
        'person_name': 'Bruce Lee', 
        'bio': 'Bruce Lee was a Hong Kong-American martial artist and actor. He was the founder of Jeet Kune Do, a hybrid martial arts philosophy drawing from different combat disciplines.',
        'creator': 'Lord Rigpea' 
    }
    return render(request, 'quotes/about.html', context)