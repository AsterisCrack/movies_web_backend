from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.db.models import Q # Importamos el operador OR
from .models import Film
from .serializers import FilmSerializer

class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmDetail(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class RateFilm(generics.UpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        film = self.get_object()
        # Actualizar la calificación de la película
        # aquí se debe implementar la lógica para calcular la nueva calificación
        # y actualizar el campo 'calification' en el modelo Film
        return super().update(request, *args, **kwargs)

class AddFilmView(generics.CreateAPIView):
    serializer_class = FilmSerializer

    def handle_exception(self, exc):
        if isinstance(exc, IntegrityError):
            return Response({"error": "Duplicate film title"}, status=status.HTTP_409_CONFLICT)
        else:
            return super().handle_exception(exc)

class SearchFilmView(generics.ListAPIView):
    serializer_class = FilmSerializer
        
    def get_queryset(self):
        title = self.request.query_params.get('title', '')
        description = self.request.query_params.get('description', '')
        genre = self.request.query_params.get('genre', '')
        director = self.request.query_params.get('director', '')
        min_calification = self.request.query_params.get('min_calification', None)
        max_calification = self.request.query_params.get('max_calification', None)

        # Construir la consulta
        query = Q()
        if title:
            query &= Q(title__icontains=title)
        if description:
            query &= Q(description__icontains=description)
        if genre:
            query &= Q(genre__icontains=genre)
        if director:
            query &= Q(director__icontains=director)
        if min_calification is not None:
            query &= Q(calification__gte=min_calification)
        if max_calification is not None:
            query &= Q(calification__lte=max_calification)

        return Film.objects.filter(query)
    
        