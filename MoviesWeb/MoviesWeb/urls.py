"""
URL configuration for MoviesWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView # Esto venia en la practica

from apps.users import views # Importar las vistas de la app users
from apps.movies import views as movies_views # Importar las vistas de la app movies

urlpatterns = [
    path("admin/", admin.site.urls),
    path('apps/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('apps/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('apps/users/', views.RegistroView.as_view(), name='registro_usuario'),
    path('apps/users/login/', views.LoginView.as_view(), name='login_usuario'),
    path('apps/users/me/', views.UsuarioView.as_view(), name='usuario'),
    path('apps/users/logout/', views.LogoutView.as_view(), name='logout_usuario'),
    path('apps/movies/', movies_views.FilmList.as_view(), name='film-list'),
    path('apps/movies/<int:pk>/', movies_views.FilmDetail.as_view(), name='film-detail'),
    path('apps/movies/<int:pk>/rate/', movies_views.RateFilm.as_view(), name='rate-film'),
    path('apps/movies/add/', movies_views.AddFilmView.as_view(), name='add-film'),
    path('apps/movies/search/', movies_views.SearchFilmView.as_view(), name='search-film'),
    path('apps/movies/delete/<int:pk>/', movies_views.DeleteFilmView.as_view(), name='delete-film'),
    path('apps/movies/update/<int:pk>/', movies_views.ModifyFilmView.as_view(), name='update-film'),
    path('apps/movies/<int:film_id>/opinions/', movies_views.AddOpinionView.as_view(), name='add_opinion'),
    path('apps/users/<int:user_id>/', views.ObtenerUsername.as_view(), name='obtener_username'),
]
