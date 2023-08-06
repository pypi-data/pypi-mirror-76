from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TamarinTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['token-type'] = 'access'
        token['pk'] = user.pk
        token['first-name'] = user.first_name
        token['last-name'] = user.last_name
        token['full-name'] = user.get_full_name()
        token['email'] = user.email
        token['username'] = user.username
        token['last-login'] = str(user.last_login)
        token['firebase-token']: getattr(user, 'firebase_token', '')

        return token


class TamarinTokenObtainPairView(TokenObtainPairView):
    serializer_class = TamarinTokenSerializer
