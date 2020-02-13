from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Twitter_Clone.tweets.forms import CreateTweetForm
from Twitter_Clone.tweets.models import Tweet


def tweet_view(request, id):
    tweet = Tweet.objects.get(pk=id)

    return render(request, 'tweet.html', {'tweet': tweet})


@login_required
def create_tweet_view(request):
    if request.method == 'POST':
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tweet = Tweet.objects.create(
                user=request.user.twitteruser,
                content=data['content']
            )
            tweet.save()

            return HttpResponseRedirect(reverse('homepage'))
    form = CreateTweetForm()
    return render(request, 'generic-form.html', {'form': form})


def tweets_view(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweets.html', {'tweets': tweets})



