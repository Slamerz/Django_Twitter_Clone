from django.shortcuts import render

from Twitter_Clone.tweets.models import Tweet
from Twitter_Clone.twitterusers.models import TwitterUser


def twitter_user_view(request, id):
    twitter_user = TwitterUser.objects.get(pk=id)
    tweets = Tweet.objects.filter(user=twitter_user)
    return render(request, 'user.html', {'twitter_user': twitter_user, 'tweets': tweets})
