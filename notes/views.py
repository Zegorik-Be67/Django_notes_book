from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views import View
from .forms import NotesForm, RegistrationForm
from .models import Notes, Tags

class UserNoteMixin:
    def get_note(self, request, **kwargs):
        note = get_object_or_404(Notes, pk = kwargs.get('pk'))
        if note.user != request.user:
            raise PermissionDenied
        return note

class ForumView(View):
    def get(self, request, *args, **kwargs):
        notes = Notes.objects.filter(is_private=False)
        return render(request, 'notes/forum.html', {'notes': notes})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if 'add_text' in request.POST:
            text = request.POST.get('input')
            if text:
                Notes.objects.create(user=request.user, note=text)
        return redirect('notes:forum')

class HomeView(LoginRequiredMixin ,View):
    def get(self, request, *args, **kwargs):
        notes_list = Notes.objects.filter(user=request.user, is_private=True)

        search = request.GET.get('search', '').strip()
        if search:
            notes_list = notes_list.filter(tags__name=search)

        # Нумерация страниц
        page_number = request.GET.get('page', 1)
        paginator = Paginator(notes_list, 10)
        notes = paginator.get_page(page_number)

        return render(request, 'notes/home.html', {'notes': notes, 'search': search})

class AddPrivateNoteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = NotesForm()
        return render(request, 'notes/add_note.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NotesForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.is_private = True
            form.save()
            return redirect('notes:home')

        return render(request, 'notes/add_note.html', {'form': form})

class EditNoteView(LoginRequiredMixin, UserNoteMixin, View):
    def get(self, request, *args, **kwargs):
        note = self.get_note(request, **kwargs)
        form = NotesForm(instance=note)
        return render(request, 'notes/edit_note.html', {'form': form})

    def post(self, request, *args, **kwargs):
        note = self.get_note(request, **kwargs)
        if 'add_tag' in request.POST:
            tag_name = request.POST.get('new_tag')
            if tag_name:
                tag, created = Tags.objects.get_or_create(name=tag_name)
                note.tags.add(tag)
                return redirect('notes:edit_note', pk=note.pk)
        elif 'save_note' in request.POST:
            form = NotesForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                return redirect('notes:home')
        form = NotesForm(instance=note)
        return render(request, 'notes/edit_note.html', {'form': form})

class DeleteNoteView(LoginRequiredMixin, UserNoteMixin, View):
    def post(self, request, *args, **kwargs):
        note = self.get_note(request, **kwargs)
        note.delete()
        return redirect('notes:home')

class RegisterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'notes/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes:home')

        return render(request, 'notes/register.html', {'form': form})