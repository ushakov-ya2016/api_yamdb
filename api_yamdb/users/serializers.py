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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value
