from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import Usuario
from apps.movies.models import Film, Opinion

class FilmAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'Test_user123',
            'password': 'Test_password123',
            'nombre': 'Test User',
            'tel': '1234567890',
            'email': 'test@example.com',
        }
        # Register a user
        response = self.client.post(reverse('registro_usuario'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Log in with the registered user
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(reverse('login_usuario'), data=login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

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

    def test_add_film(self):
        response = self.client.post(reverse('add-film'), data=self.film_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_film(self):
        response = self.client.get(reverse('search-film'), {'title': 'Test Film'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Test Film' in response.data[0]['title'])

    def test_delete_film(self):
        response = self.client.delete(reverse('delete-film', kwargs={'pk': self.film.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Film.objects.filter(pk=self.film.pk).exists())

    def test_add_opinion(self):
        opinion_data = {'comment': 'This is a test opinion', 'calification': 9}
        response = self.client.post(reverse('add_opinion', kwargs={'film_id': self.film.pk}), data=opinion_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Opinion.objects.filter(film=self.film, comment='This is a test opinion').exists())
