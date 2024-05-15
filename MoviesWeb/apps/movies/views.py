from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.db.models import Q # Importamos el operador OR
from .models import Film, FilmRating
from .serializers import FilmSerializer, OpinionSerializer
from rest_framework.authtoken.models import Token
from apps.users.models import Usuario
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied

class FilmList(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    
class AddOpinionView(generics.CreateAPIView):
    serializer_class = OpinionSerializer

    def perform_create(self, serializer):
        # Obtener la película asociada a la opinión
        film = get_object_or_404(Film, id=self.kwargs['film_id'])

        # Verificar si hay una sesión activa
        token_key = self.request.COOKIES.get('session')
        if not token_key:
            return Response({'error': 'No active session.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener el usuario asociado al token
        user_token = Token.objects.filter(key=token_key).first()
        if not user_token:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener el usuario asociado al token
        user = get_object_or_404(Usuario, auth_token=user_token)

        # Guardar la opinión asociada al usuario y la película
        serializer.save(user=user, film=film)

        # Calcular la nueva calificación global de la película
        opinions = film.opinions.all()
        total_calification = sum(opinion.calification for opinion in opinions)
        average_calification = total_calification / len(opinions)

        # Actualizar la calificación global de la película
        film.calification = average_calification
        film.save()



class FilmDetail(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class RateFilm(generics.UpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def update(self, request, *args, **kwargs):
        # Verificar si hay una sesión activa
        token_key = request.COOKIES.get('session')
        if not token_key:
            return Response({'error': 'No active session.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener el usuario asociado al token
        user_token = Token.objects.filter(key=token_key).first()
        if not user_token:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener la película que se va a calificar
        film = self.get_object()
        
        # Obtener la nueva calificación proporcionada por el usuario
        new_calification = request.data.get('calification')
        if new_calification is None:
            return Response({'error': 'No calification provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener el usuario asociado al token
        user = get_object_or_404(Usuario, auth_token=user_token)
        
        # Calcular la nueva calificación
        film_rating = FilmRating.objects.create(user=user, film=film, calification=new_calification)
        ratings = FilmRating.objects.filter(film=film)
        total_ratings = ratings.count()
        total_calification = sum([rating.calification for rating in ratings])
        average_calification = total_calification / total_ratings
        
        # Actualizar el campo 'calification' en el modelo Film
        film.calification = average_calification
        film.save()
        
        # Devolver una respuesta indicando que la calificación se ha actualizado correctamente
        return Response({'message': 'Film calification updated successfully.'}, status=status.HTTP_200_OK)
    

class AddFilmView(generics.CreateAPIView):
    serializer_class = FilmSerializer

    def create(self, request, *args, **kwargs):
        # Verificar si hay una sesión activa
        token_key = request.COOKIES.get('session')
        if not token_key:
            return Response({'error': 'No active session.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener el usuario asociado al token
        user_token = Token.objects.filter(key=token_key).first()
        if not user_token:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar si el usuario tiene permisos de administrador
        user = get_object_or_404(Usuario, auth_token=user_token)
        if user.username != "admin":
            raise PermissionDenied("Only admin can add films.")

        # Obtener los datos de la solicitud
        title = request.data.get('title', '')
        link_image = request.data.get('link_image', '')
        description = request.data.get('description', '')
        genre = request.data.get('genre', '')
        director = request.data.get('director', '')
        calification = float(request.data.get('calification', 0))
        opinions = request.data.get('opinions', [])

        # Crear un diccionario con los datos de la película
        film_data = {
            'title': title,
            'link_image': link_image,
            'description': description,
            'genre': genre,
            'director': director,
            'calification': calification,
            'opinions': opinions
        }

        # Crear el serializador con los datos de la película
        serializer = self.get_serializer(data=film_data)
        serializer.is_valid(raise_exception=True)

        # Guardar la película
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


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
    

class DeleteFilmView(generics.DestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        identifier = self.kwargs.get(self.lookup_url_kwarg)
        
        try:
            return self.queryset.get(id=identifier)
        except (ValueError, Film.DoesNotExist):
            pass
        
        try:
            return self.queryset.get(title=identifier)
        except Film.DoesNotExist:
            raise ValidationError({'detail': 'Not found.'})

    def delete(self, request, *args, **kwargs):
        # Verificar si hay una sesión activa
        token_key = request.COOKIES.get('session')
        if not token_key:
            return Response({'error': 'No active session.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener el usuario asociado al token
        user_token = Token.objects.filter(key=token_key).first()
        if not user_token:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar si el usuario tiene permisos de administrador
        user = get_object_or_404(Usuario, auth_token=user_token)
        if user.username != "admin":
            raise PermissionDenied("Only admin can delete films.")

        film = self.get_object()
        film.delete()
        return Response({'detail': 'Film deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ModifyFilmView(generics.UpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verificar si hay una sesión activa
        token_key = request.COOKIES.get('session')
        if not token_key:
            return Response({'error': 'No active session.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener el usuario asociado al token
        user_token = Token.objects.filter(key=token_key).first()
        if not user_token:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar si el usuario tiene permisos de administrador
        user = get_object_or_404(Usuario, auth_token=user_token)
        if user.username != "admin":
            raise PermissionDenied("Only admin can modify films.")

        # Obtener los datos actuales de la película
        current_data = self.get_serializer(instance).data

        # Obtener los datos a actualizar de la solicitud
        updated_data = {}
        for key, value in request.data.items():
            if value is not None and value != '':
                updated_data[key] = value
            else:
                # Si el valor es None, mantener el valor actual de la película
                updated_data[key] = current_data.get(key)

        # Validar que haya al menos un campo en la solicitud
        if not updated_data:
            raise ValidationError("No data provided for update.")

        serializer = self.get_serializer(instance, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)





    
    

