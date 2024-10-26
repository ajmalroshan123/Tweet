from django.shortcuts import render, get_object_or_404
from .models import Tweet
from .forms import TweetForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')    
    return render(request, 'tweet_list.html', {'tweets': tweets})

def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            form.save()
            return 
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})    