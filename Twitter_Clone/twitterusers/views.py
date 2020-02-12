from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def twitter_user_view(request, id):
    return HttpResponse(f"user is {id}")
