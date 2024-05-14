from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status, serializers
from rest_framework.test import APIClient
from apps.users.serializers import UsuarioSerializer, LoginSerializer

User = get_user_model()


class UsuarioSerializerTest(TestCase):
    def test_validate_password_with_short_password(self):
        serializer = UsuarioSerializer()
        with self.assertRaisesMessage(
            serializers.ValidationError, "Invalid password format"
        ):
            serializer.validate_password("Pass1")

    def test_validate_password_without_special_characters(self):
        serializer = UsuarioSerializer()
        with self.assertRaisesMessage(
            serializers.ValidationError, "Invalid password format"
        ):
            serializer.validate_password("Password123")

    def test_validate_password_without_digits(self):
        serializer = UsuarioSerializer()
        with self.assertRaisesMessage(
            serializers.ValidationError, "Invalid password format"
        ):
            serializer.validate_password("Password@")

    def test_validate_password_without_uppercase(self):
        serializer = UsuarioSerializer()
        with self.assertRaisesMessage(
            serializers.ValidationError, "Invalid password format"
        ):
            serializer.validate_password("password@123")

    def test_validate_password_with_valid_password(self):
        serializer = UsuarioSerializer()
        validated_password = serializer.validate_password("Password@123")
        self.assertEqual(validated_password, "Password@123")


class LoginSerializerTest(TestCase):
    def test_valid_login_data(self):
        user = User.objects.create(username="testuser")
        user.set_password("testpassword")
        user.save()

        serializer = LoginSerializer(
            data={"username": "testuser", "password": "testpassword"}
        )
        self.assertTrue(serializer.is_valid())
        self.assertTrue("user" in serializer.validated_data)

    def test_invalid_login_data(self):
        serializer = LoginSerializer(
            data={"username": "testuser", "password": "testpassword"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertTrue("non_field_errors" in serializer.errors)

    def test_login_with_incomplete_data(self):
        serializer = LoginSerializer(data={"username": "testuser"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_login_with_nonexistent_user(self):
        serializer = LoginSerializer(
            data={"username": "nonexistent", "password": "password"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_login_with_wrong_password(self):
        user = User.objects.create(username="testuser")
        user.set_password("testpassword")
        user.save()

        serializer = LoginSerializer(
            data={"username": "testuser", "password": "wrongpassword"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class RegistroUsuarioTest(TestCase):
    def test_registro_usuario_sin_password_en_respuesta(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "nombre": "Usuario",
            "tel": "123456789",
            "email": "test@example.com",
            "password": "Password@123",
        }
        response = client.post("/apps/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)

    def test_registro_usuario_con_datos_incompletos(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "email": "test@example.com"
            # Falta 'password', 'nombre', 'tel'
        }
        response = client.post("/apps/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registro_usuario_con_email_invalido(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "nombre": "Usuario",
            "tel": "123456789",
            "email": "invalidemail",
            "password": "Password@123",
        }
        response = client.post("/apps/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registro_usuario_con_username_existente(self):
        user = User.objects.create(username="testuser", email="existing@example.com")
        user.set_password("Password@123")
        user.save()

        client = APIClient()
        data = {
            "username": "testuser",
            "nombre": "Usuario",
            "tel": "123456789",
            "email": "new@example.com",
            "password": "Password@123",
        }
        response = client.post("/apps/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)