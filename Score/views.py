from itertools import count
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache

def getScore(request):
    if cache.get("score"):
        data=cache.get("score")
        return JsonResponse(data)
    else:
        if cache.get("recent"):
            data=cache.get("recent")
            return JsonResponse(data)
        else:
            data={
                'status':False
            }
            return JsonResponse(data)

def pointsTable(request):
    data=cache.get("points")
    return JsonResponse(data)

def clear(request):
    cache.clear()
    print(cache.get("match"))
    print(cache.get("score"))
    return HttpResponse("")