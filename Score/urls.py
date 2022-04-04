from django.urls import path
from . import views
urlpatterns=[
    path('scorecard/', views.getScore, name="getScore"),
    path('clear/',views.clear,name="clear"),
]