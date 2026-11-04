from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.home , name='home'),
    path('add_note/', views.add_note, name='add_note'),
    path('<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('<int:pk>/delete/', views.delete_note, name='delete_note'),

    path('register/', views.registration, name='register'),
]