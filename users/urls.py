from django.urls import include, path
from . import views
# from ..rreports import views as repv

app_name = 'users'

urlpatterns = [
    path('login/', views.userLogin, name="login"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.userLogout, name='logout'),
]
