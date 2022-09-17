from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',
        )
        model = User


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]'
    )
    confirmation_code = serializers.CharField(required=True)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()), ]
    )
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]',
        validators=[UniqueValidator(queryset=User.objects.all()), ]
    )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        elif User.objects.filter(username=data.get('username')):
            if User.objects.get(
                username=data.get('username')
            ).email != data.get('email'):
                raise serializers.ValidationError('Такой username уже занят')
        elif User.objects.filter(email=data.get('email')):
            if User.objects.get(
                email=data.get('email')
            ).username != data.get('username'):
                raise serializers.ValidationError('Такой email уже занят')
        return data

