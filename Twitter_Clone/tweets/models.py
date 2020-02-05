from django.db import models
from django.utils import timezone
from Twitter_Clone.twitterusers.models import TwitterUser


class Tweet(models.Model):
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    date_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
