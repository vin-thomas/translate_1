from django.urls import include, path
from . import views
# from ..rreports import views as repv

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('gauth/', views.gauth, name="gauth"),
    path('logout/', views.logout_view, name='logout'),
]
