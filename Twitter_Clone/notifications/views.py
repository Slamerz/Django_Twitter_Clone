from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Twitter_Clone.notifications.models import Notification
from Twitter_Clone.twitterusers.models import TwitterUser


@login_required
def notifications_view(request):
    twitter_user = TwitterUser.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=twitter_user, viewed=False)

    for notification in notifications:
        notification.viewed = True
        notification.save()
    return render(request, 'notifications.html', {'notifications': notifications})
