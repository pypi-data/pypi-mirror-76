from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TamarinTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
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
        token.update(data)
        return token


class TamarinTokenObtainPairView(TokenObtainPairView):
    serializer_class = TamarinTokenSerializer
