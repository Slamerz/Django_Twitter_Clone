from django import forms

from Twitter_Clone.tweets.models import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
