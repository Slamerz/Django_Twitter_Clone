import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Twitter_Clone.notifications.models import Notification
from Twitter_Clone.tweets.forms import CreateTweetForm
from Twitter_Clone.tweets.models import Tweet
from Twitter_Clone.twitterusers.models import TwitterUser


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
            notified_users = re.findall(r'@(\w+)', data['content'])
            if notified_users:
                for notify in notified_users:
                    twitter_user = TwitterUser.objects.get(user=User.objects.get(username=notify))
                    if twitter_user:
                        Notification.objects.create(
                            user=twitter_user,
                            tweet=tweet,
                            viewed=False
                        )

            return HttpResponseRedirect(reverse('homepage'))
    form = CreateTweetForm()
    return render(request, 'generic-form.html', {'form': form})


def tweets_view(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweets.html', {'tweets': tweets})



