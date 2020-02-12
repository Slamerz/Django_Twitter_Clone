from django.http import HttpResponse
from django.shortcuts import render

from Twitter_Clone.tweets.models import Tweet


def tweet_view(request, id):
    tweet = Tweet.objects.get(pk=id)

    return render(request, 'tweet.html', {'tweet': tweet})



