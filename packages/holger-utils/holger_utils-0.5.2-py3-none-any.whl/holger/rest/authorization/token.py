from rest_framework.serializers import Serializer, CharField, ValidationError
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.conf import settings
from jose import jwt


class TamarinTokenSerializer(Serializer):
    user_id = CharField(write_only=True)
    token = CharField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        User = get_user_model()
        users = User.objects.filter(pk=user_id)
        if not users.exists():
            error = {
                'user': "user not found"
            }
            raise ValidationError(error)
        user = users.last()
        token = self.get_token(user)
        attrs['token'] = token
        return attrs

    @staticmethod
    def get_token(user):
        data = {
            'token-type': 'access',
            'pk': user.pk,
            'first-name': user.first_name,
            'last-name': user.last_name,
            'full-name': user.get_full_name(),
            'email': user.email,
            'username': user.username,
            'last-login': str(user.last_login),
            'firebase-token': getattr(user, 'firebase_token', ''),
            'exp': datetime.now() + timedelta(days=1)
        }
        key = getattr(settings, 'TAMARIN_JWT_KEY', settings.SECRET_KEY)
        token = jwt.encode(data, key)
        return token
