from django.urls import path

from judge import views

urlpatterns = [
    path('compile', views.index, name='index'),
    path('', views.home, name='home'),
    path('addtestcase/', views.addTestCase, name='addtestcase'),
    path('code/<str:code>', views.submitcode, name='submitcode'),
    path('createquestion',views.createQuestion, name = 'createquestion')
]
