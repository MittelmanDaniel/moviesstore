from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='petitions.index'),
    path('create/', views.create, name='petitions.create'),
    path('<int:id>/', views.show, name='petitions.show'),
    path('<int:id>/yes/', views.vote_yes, name='petitions.vote_yes'),
    path('<int:id>/no/', views.vote_no, name='petitions.vote_no'),
]
