from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from Twitter_Clone.authentication.forms import CreateUserForm
from Twitter_Clone.notifications.models import Notification
from Twitter_Clone.tweets.models import Tweet
from Twitter_Clone.twitterusers.models import TwitterUser


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        following = list(self.request.user.twitteruser.following.all())
        tweets = []
        for user in following:
            tweets += Tweet.objects.filter(user=user)
        tweets = sorted(tweets, key=lambda tweet: tweet.date_published, reverse=True)
        notifications = Notification.objects.filter(user=TwitterUser.objects.get(user=self.request.user), viewed=False)

        context['tweets'] = tweets
        context['notifications'] = notifications
        return context


class LoginUserView(LoginView):
    template_name = 'generic-form.html'
    success_url = 'index.html'
    extra_context = {'allow_register': True}


@method_decorator(login_required, name='dispatch')
class LogoutUserView(LogoutView):
    next_page = '/'


class CreateUserView(CreateView):
    template_name = 'generic-form.html'
    form_class = CreateUserForm

    def form_valid(self, form):
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
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('homepage'))
