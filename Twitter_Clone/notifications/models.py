from django.db import models
from Twitter_Clone.twitterusers.models import TwitterUser
from Twitter_Clone.tweets.models import Tweet


class Notification(models.Model):
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return self.tweet.content
