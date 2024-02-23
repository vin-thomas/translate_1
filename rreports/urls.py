from django.urls import path
from . import views


app_name = 'rreports'
urlpatterns =[
    path("", views.index, name = "index")
]
