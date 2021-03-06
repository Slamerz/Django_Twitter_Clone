from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, reverse

from Twitter_Clone.authentication.forms import LoginForm, CreateUserForm
from Twitter_Clone.notifications.models import Notification
from Twitter_Clone.tweets.models import Tweet
from Twitter_Clone.twitterusers.models import TwitterUser


@login_required
def index_view(request):
    following = list(request.user.twitteruser.following.all())
    tweets = []
    for user in following:
        tweets += Tweet.objects.filter(user=user)
    tweets = sorted(tweets, key=lambda tweet: tweet.date_published, reverse=True)
    notifications = Notification.objects.filter(user=TwitterUser.objects.get(user=request.user), viewed=False)
    return render(request, 'index.html', {'tweets': tweets, 'notifications': notifications})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage'))
            )
    form = LoginForm()
    return render(
        request,
        'generic-form.html',
        {'form': form, 'allow_register': True}
    )


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def create_user_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            twitter_user = TwitterUser.objects.create(
                user=user
            )
            twitter_user.following.add(twitter_user)
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
    form = CreateUserForm()
    return render(request, 'generic-form.html', {'form': form})


