from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('3x3', views.board_3x3, name='board_3x3'),
    path('4x4', views.board_4x4, name='board_4x4'),
]
