from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from Twitter_Clone.tweets.models import Tweet
from Twitter_Clone.twitterusers.models import TwitterUser


def twitter_user_view(request, id):
    twitter_user = TwitterUser.objects.get(pk=id)
    tweets = Tweet.objects.filter(user=twitter_user)
    return render(request, 'user.html', {'twitter_user': twitter_user, 'tweets': tweets})


@login_required
def follow_view(request, id):
    current_user = TwitterUser.objects.get(user=request.user)
    user_to_follow = TwitterUser.objects.get(pk=id)
    current_user.following.add(user_to_follow)
    current_user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unfollow_view(request, id):
    current_user = TwitterUser.objects.get(user=request.user)
    user_to_unfollow = TwitterUser.objects.get(pk=id)
    current_user.following.remove(user_to_unfollow)
    current_user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
