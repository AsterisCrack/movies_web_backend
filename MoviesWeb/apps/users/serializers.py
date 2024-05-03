import re
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from apps.users import models # Modificado para importar el modelo de la app users

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Usuario
        fields = ['id', 'username', 'password', 'nombre', 'tel', 'email']

        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate_password(self, value):
        valid_password = True

        if len(value) < 8 or not re.match(r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).*$', value):
            valid_password = False
        
        if valid_password:
            return value
        else:
            raise exceptions.ValidationError('Invalid password format')

    def create(self, validated_data):
        username = validated_data.pop('username')  # Extraemos el username de los datos validados
        return models.Usuario.objects.create_user(username=username, **validated_data)

    def update(self, instance, validated_data):
        if (validated_data.get('password')):
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
                return data
            else:
                raise exceptions.ValidationError('Unable to login with provided credentials')
        
        