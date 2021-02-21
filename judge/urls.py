from django.urls import path

from judge import views

urlpatterns = [
    path('', views.index, name='index'),

]
