from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.ForumView.as_view(), name='forum'),
    path('home/', views.HomeView.as_view() , name='home'),
    path('add_note/', views.AddPrivateNoteView.as_view(), name='add_note'),
    path('<int:pk>/edit/', views.EditNoteView.as_view(), name='edit_note'),
    path('<int:pk>/delete/', views.DeleteNoteView.as_view(), name='delete_note'),

    path('register/', views.RegisterView.as_view(), name='register'),
]