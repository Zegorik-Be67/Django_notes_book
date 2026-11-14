from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, F
from rest_framework.views import APIView
from .models import Notes, LikedNotes, FavoriteNotes, Comments
from .serializers import NotesPublicSerializer, NotesPrivateSerializer, FavoriteNotesSerializer, LikedNotesSerializer, CommentSerializer


class PublicNotesList(generics.ListCreateAPIView):
    serializer_class = NotesPublicSerializer

    def get_queryset(self):
        return Notes.objects.filter(is_private=False).select_related('user').annotate(likes_notes=Count('liked_notes'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_private=False)

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesPublicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)

class HomeNotesList(generics.ListCreateAPIView):
    serializer_class = NotesPrivateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user , is_private=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_private=True)

class HomeNotesDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesPrivateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user, is_private=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_private=True)

class LikedNotesList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        note_id = kwargs.get('pk')
        note = get_object_or_404(Notes, pk=note_id)
        like, cr = FavoriteNotes.objects.get_or_create(user=request.user, note=note)
        if cr:
            Notes.objects.filter(pk=note.pk).update(count_like=F('count_like') + 1)
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        note_id = kwargs.get('pk')
        note = get_object_or_404(Notes, pk=note_id)
        like = FavoriteNotes.objects.filter(user=request.user, note=note).first()
        if like:
            like.delete()
            Notes.objects.filter(pk=note.pk).update(count_like=F('count_like') - 1)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

class FavoriteNotesList(generics.ListCreateAPIView):
    serializer_class = FavoriteNotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteNotes.objects.filter(user=self.request.user).select_related('note', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteNotesDetail(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteNotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteNotes.objects.filter(user=self.request.user)

class CommentsList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        note = get_object_or_404(Notes, pk=self.kwargs['note_pk'], is_private=False)
        return Comments.objects.filter(note=note).select_related('user', 'note')

    def perform_create(self, serializer):
        note = get_object_or_404(Notes, pk=self.kwargs['note_pk'], is_private=False)
        serializer.save(user=self.request.user, note=note)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.filter(user=self.request.user, pk=self.kwargs['pk'])