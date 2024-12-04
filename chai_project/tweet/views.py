from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request, 'index.html')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistration()

    return render(request, 'registration/register.html', {'form': form})     

# List the tweets
def tweet_list(request):
    
    tweets = Tweet.objects.all().order_by('-created_at')    
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create the tweet
@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user 
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})  


# edit the tweet
@login_required
def edit_tweet(request, tweet_id):

    tweet = get_object_or_404(Tweet, id = tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance = tweet)

        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            
            return redirect('tweet_list')

    else:
        form = TweetForm(instance = tweet)
    
    return render(request, 'tweet_form.html', {'form': form})        


# Delete tweet
@login_required
def delete_tweet(request, tweet_id):

    tweet = get_object_or_404(Tweet, id = tweet_id, user = request.user)
    
    if request.method == 'POST':
        tweet.delete()

        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})    