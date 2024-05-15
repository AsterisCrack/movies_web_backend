from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from apps.users import (
    serializers,
)  # Modificado para importar el serializador de la app users
from drf_spectacular.utils import extend_schema, OpenApiResponse
import rest_framework.exceptions


# Create your views here.
class RegistroView(generics.CreateAPIView):
    serializer_class = serializers.UsuarioSerializer

    def handle_exception(self, exc):
        if isinstance(exc, IntegrityError):
            return Response({"error": "Used mail"}, status=status.HTTP_409_CONFLICT)

        else:
            return super().handle_exception(exc)


class LoginView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            response = Response(
                {"message": "Login successful"}, status=status.HTTP_201_CREATED
            )
            response.set_cookie(
                key="session",
                value=token.key,
                secure=True,
                httponly=True,
                samesite="lax",
            )
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UsuarioView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UsuarioSerializer

    def get_object(self):
        # Obtener el usuario autenticado a través del token de sesión
        token_key = self.request.COOKIES.get("session")
        token = Token.objects.filter(key=token_key).first()
        if token:
            return token.user
        else:
            return None

    def get(self, request, *args, **kwargs):
        print(request.COOKIES)
        # Verificar si se proporcionó un token de sesión
        if not self.get_object():
            return Response(
                {"error": "No active session. Get action not valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Verificar si se proporcionó un token de sesión
        if not self.get_object():
            return Response(
                {"error": "No active session. Delete action not valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().delete(request, *args, **kwargs)

    def handle_exception(self, exc):
        # Manejar específicamente ObjectDoesNotExist y devolver un 404 Not Found
        if isinstance(exc, ObjectDoesNotExist):
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        # Llamar al manejador de excepciones por defecto para otros tipos de excepciones
        return super().handle_exception(exc)

    def put(self, request, *args, **kwargs):
        # Verificar si se proporcionó un token de sesión
        if not self.get_object():
            return Response(
                {"error": "No active session. Put action not valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Verificar si se proporcionó un token de sesión
        if not self.get_object():
            return Response(
                {"error": "No active session. Patch action not valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().patch(request, *args, **kwargs)


class LogoutView(generics.DestroyAPIView):
    def delete(self, request):
        token_key = request.COOKIES.get("session")

        if not token_key:
            return Response(
                {"error": "No active session. Delete action not valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        else:
            Token.objects.filter(key=token_key).delete()

            response = Response(
                {"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT
            )

            response.delete_cookie("session")

        return response
