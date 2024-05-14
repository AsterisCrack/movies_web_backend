from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.movies.models import Film, Opinion
from apps.users.serializers import UsuarioSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class FilmAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'admin',
            'password': 'Password123',
            'nombre': 'admin',
            'tel': '1234567890',
            'email': 'test@example.com',
        }
        
        user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])
        user.save()
        
        serializer = LoginSerializer(data={'username': self.user_data['username'], 'password': self.user_data['password']})
        self.assertTrue(serializer.is_valid())
        self.assertTrue('user' in serializer.validated_data)
        # Iniciar sesión con el usuario registrado
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post("/apps/users/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.film_data = {
            'title': 'Test Film',
            'description': 'This is a test film',
            'genre': 'Test Genre',
            'director': 'Test Director',
            'calification': 0,
        }
        self.film = Film.objects.create(**self.film_data)

    def test_get_film_list(self):
        response = self.client.get(reverse('film-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_film_detail(self):
        response = self.client.get(reverse('film-detail', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rate_film(self):
        rating_data = {'calification': 8}
        response = self.client.put(reverse('rate-film', kwargs={'pk': self.film.pk}), data=rating_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.get(pk=self.film.pk).calification, 8)

    def test_search_film(self):
        response = self.client.get(reverse('search-film'), {'title': 'Test Film'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Test Film' in response.data[0]['title'])

    def test_delete_film(self):
        response = self.client.delete(reverse('delete-film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Film.objects.filter(pk=self.film.pk).exists())

    def test_add_film(self):
        film_data = {
            'title': 'Test Film' + str(Film.objects.count() + 1),
            'description': 'This is a test film',
            'genre': 'Test Genre',
            'director': 'Test Director',
            'calification': 0,
            'opinions': []  # Assuming opinions is a required field and should be provided
        }
        response = self.client.post(reverse('add-film'), data=film_data)
        if response.status_code != status.HTTP_201_CREATED:
            print("Add Film Error:", response.data)  # Print serializer errors if validation fails
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_opinion(self):
        # Get the primary key value of the user created in setUp
        user_id = User.objects.get(username=self.user_data['username']).pk
        opinion_data = {'user': user_id, 'comment': 'This is a test opinion', 'calification': 9}
        response = self.client.post(reverse('add_opinion', kwargs={'film_id': self.film.pk}), data=opinion_data)
        if response.status_code != status.HTTP_201_CREATED:
            print("Add Opinion Error:", response.data)  # Print serializer errors if validation fails
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_modify_film(self):
        # Update film data
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'genre': 'Updated Genre',
            'director': 'Updated Director',
            'calification': 7.5,  # Update calification
        }

        # Login as admin
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post("/apps/users/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure the film exists
        self.assertTrue(Film.objects.filter(pk=self.film.pk).exists())

        # Modify the film
        response = self.client.put(reverse('update-film', kwargs={'pk': self.film.pk}), data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if film data has been updated
        updated_film = Film.objects.get(pk=self.film.pk)
        self.assertEqual(updated_film.title, updated_data['title'])
        self.assertEqual(updated_film.description, updated_data['description'])
        self.assertEqual(updated_film.genre, updated_data['genre'])
        self.assertEqual(updated_film.director, updated_data['director'])
        self.assertEqual(updated_film.calification, updated_data['calification'])



