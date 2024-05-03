from django.contrib import admin

# Register your models here.

from apps.movies.models import Film
from apps.users.models import Usuario

# Registra el modelo Film
admin.site.register(Film)

# Define la clase UsuarioAdmin para personalizar el modelo Usuario en el panel de administración
class UsuarioAdmin(admin.ModelAdmin):
    # Lista de campos que se mostrarán en la vista de lista
    list_display = ('nombre', 'tel', 'email')

# Registra el modelo Usuario con el UsuarioAdmin personalizado
admin.site.register(Usuario, UsuarioAdmin)