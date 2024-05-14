from django.conf import settings
from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=50, default='')
    calification = models.FloatField(default=0)

    def __str__(self):
        return self.title

class FilmRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, related_name='ratings', on_delete=models.CASCADE)
    calification = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.film.title} - {self.calification}"


class Opinion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, related_name='opinions', on_delete=models.CASCADE)
    comment = models.TextField()
    calification = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.film.title} - {self.calification} - {self.created_at}"
