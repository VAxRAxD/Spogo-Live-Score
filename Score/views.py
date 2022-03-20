from itertools import count
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from . import fetch

def getScore(request):
    if cache.get("score"):
        data=cache.get("score")
        return JsonResponse(data)
    else:
        data={
            'status':'No Ongoing Matches'
        }
        return JsonResponse(data)