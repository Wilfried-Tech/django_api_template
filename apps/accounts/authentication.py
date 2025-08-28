from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAndCookieAuthentication(JWTAuthentication):

    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            raw_token = request.COOKIES.get('access_token')
            if raw_token is None:
                return None
            validated_token = self.get_validated_token(raw_token)
            result = self.get_user(validated_token), validated_token

        return result
