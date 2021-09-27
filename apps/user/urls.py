from django.urls import path

from apps.user.views import RegisterView, LoginView, logout

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('out/', logout, name='out'),
    path('forget/', LoginView.as_view(), name='forget'),
]


