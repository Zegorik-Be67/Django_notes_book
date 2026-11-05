from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import NotesForm, RegistrationForm
from .models import Notes, Tags

@login_required
def home(request):
    notes = Notes.objects.filter(user_id=request.user)
    search = request.GET.get('search', '').strip()
    if search:
        notes = notes.filter(tags__name=search)
    return render(request, 'notes/home.html', {'notes': notes, 'search': search})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            task = form.save(commit = False)
            task.user = request.user
            task.save()
            return redirect('notes:home')
    else:
        form = NotesForm()

    return render(request, 'notes/add_note.html', {'form': form})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    form = NotesForm(request.POST or None, instance=note)
    if request.method == 'POST':
        if 'add_tag' in request.POST:
            tag_name = request.POST.get('new_tag')
            if tag_name:
                Tags.objects.get_or_create(name=tag_name)
                return redirect('notes:edit_note', pk=note.pk)
        elif 'save_note' in request.POST:
            form = NotesForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                return redirect('notes:home')

    return render(request, 'notes/edit_note.html', {'form': form})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    note.delete()
    return redirect('notes:home')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes:home')
    else:
        form = RegistrationForm()

    return render(request, 'notes/register.html', {'form': form})