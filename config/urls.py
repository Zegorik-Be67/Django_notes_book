"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from notes import views as notes_views, api_views
from django.urls import path, include
from notes.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', notes_views.ForumView.as_view() , name='forum'),
    path('notes/drf-notes/forum/', api_views.PublicNotesList.as_view(), name='public-notes-list'),
    path('notes/drf-notes/forum/<int:pk>/', api_views.NoteDetail.as_view(), name='public-note-detail'),
    path('notes/drf-notes/forum/<int:pk>/like/', api_views.LikedNotesList.as_view(), name='like-notes-list'),
    path('notes/drf-notes/forum/<int:note_pk>/comments/', api_views.CommentsList.as_view(), name='comments-list'),
    path('notes/drf-notes/forum/<int:note_pk>/comments/<int:pk>/edit/', api_views.CommentDetail.as_view(),name='comments-detail'),
    path('notes/drf-notes/home/', api_views.HomeNotesList.as_view(), name='home-notes-list'),
    path('notes/drf-notes/home/<int:pk>/', api_views.NoteDetail.as_view(), name='note-detail'),
    path('notes/drf-notes/home/favorites/', api_views.FavoriteNotesList.as_view(), name='favorites-list'),
    path('notes/drf-notes/home/favorites/<int:pk>/delete', api_views.FavoriteNotesDetail.as_view(), name='favorites-detail'),

    path('notes/', include('notes.urls', namespace='notes')),

    path('login/', auth_views.LoginView.as_view(template_name='register/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]