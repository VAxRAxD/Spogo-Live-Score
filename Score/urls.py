from django.urls import path
from . import views
urlpatterns=[
    path('scorecard/', views.getScore, name="getScore"),
    path('points/',views.pointsTable,name="pointsTable")
]