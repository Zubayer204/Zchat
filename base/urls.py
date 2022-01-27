from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),
    # path('create_member/', views.create_user),
    path('create_room/', views.create_room),
    path('get_member/', views.get_member),
    path('delete_member/', views.delete_member),
    path('enter_room/', views.enter_room)
]