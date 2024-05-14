from django.urls import path
from . import views


app_name = 'rreports_2'
urlpatterns =[
    path("", views.index, name = "index"),
    path("translate/", views.te, name = "translate")
]