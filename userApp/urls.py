from django.urls import path
from . import views as vw

urlpatterns = [
    path('signup/', vw.signupView, name='signup'),
    path('profile/', vw.userProfileView, name="profile")
]
