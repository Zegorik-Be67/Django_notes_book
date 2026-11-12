from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.models import Notes, LikedNotes
from notes.serializers import NotesSerializer, NoteSerializer

class UserNotesMixin:
    def get_note(self, request, is_private=None, **kwargs):
        note = get_object_or_404(Notes, pk=kwargs.get('pk'), is_private=is_private)
        if note.user != request.user:
            raise PermissionDenied
        return note

class NotesListApiView(APIView):
    def get(self, request, *args, **kwargs):
        notes = Notes.objects.filter(is_private=False).select_related('user')
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, is_private=False)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class NoteOperationsApiView(UserNotesMixin, APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        note = self.get_note(request, is_private=False, **kwargs)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = NoteSerializer(instance=self.get_note(request, is_private=False, **kwargs), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        note = self.get_note(request, is_private=False, **kwargs)
        note.delete()
        return Response(status=204)

class HomeApiView(UserNotesMixin, APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        notes = Notes.objects.filter(is_private=True, user=request.user).select_related('user').prefetch_related('tags')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, is_private=True)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class HomeOperationsApiView(UserNotesMixin, APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        note = self.get_note(request, is_private=True, **kwargs)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = NoteSerializer(instance=self.get_note(request, is_private=True, **kwargs), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        note = self.get_note(request, is_private=True, **kwargs)
        note.delete()
        return Response(status=204)

class LikedNotesApiView(UserNotesMixin, APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        note = self.get_note(request, is_private=False, **kwargs)
        if LikedNotes.objects.filter(user=request.user, note=note).exists():
            raise PermissionDenied
        LikedNotes.objects.create(user=request.user, note=note)
        Notes.objects.filter(pk=note.pk).update(count_likes=F('count_likes') + 1)
        return Response(note.count_likes, status=200)

    def delete(self, request, *args, **kwargs):
        note = self.get_note(request, is_private=False, **kwargs)
        if LikedNotes.objects.filter(user=request.user, note=note).exists():
            LikedNotes.objects.filter(user=request.user, note=note).delete()
            Notes.objects.filter(pk=note.pk).update(count_likes=F('count_likes') - 1)
            return Response(status=204)
        return Response({"error":"Вы не лайкали эту заметку!"}, status=400)