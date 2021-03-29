from django.contrib.auth import views
from django.urls import path

from authy.views import SignUpView, EditProfileView, ProfileView

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='authy/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView, name='signup'),
    path('viewProfile/<pk>', ProfileView, name='viewProfile'),
    path('editProfile/', EditProfileView, name='editProfile'),
]
