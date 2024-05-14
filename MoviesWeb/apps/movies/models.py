from django.db import models

# Create your models here.


class Film(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=50, default='')
    calification = models.FloatField(default=0)  # Almacena la calificación promedio de la película

    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title