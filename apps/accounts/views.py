from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CreateUserSerializer, UserTokensSerializer, UserRefreshTokenSerializer
from .serializers import PasswordResetConfirmSerializer, PasswordResetSerializer, PasswordChangeSerializer, \
    UserSerializer
from .throttles import PasswordResetRateThrottle, PasswordResetIPThrottle


@extend_schema(
    tags=["Authentification"],
)
class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Authentification"],
)
class AccountView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Authentification"],
)
class PasswordResetView(GenericAPIView):
    permission_classes = []
    throttle_classes = [PasswordResetRateThrottle, PasswordResetIPThrottle]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Authentification"],
)
class PasswordResetConfirmView(GenericAPIView):
    permission_classes = []
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetTokensInCookieMixin(GenericAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            response.set_cookie(
                key='access_token',
                value=response.data['access'],
                samesite='Lax',
                httponly=not settings.DEBUG,
                secure=not settings.DEBUG,
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            )
            if 'refresh' in response.data:
                response.set_cookie(
                    key='refresh_token',
                    value=response.data['refresh'],
                    samesite='Lax',
                    httponly=not settings.DEBUG,
                    secure=not settings.DEBUG,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                )
        return super().finalize_response(request, response, *args, **kwargs)


@extend_schema(
    request=UserRefreshTokenSerializer,
    description=_('Vous pouvez utiliser `refresh_token` dans les cookie à la place')
)
class UserTokensInCookieMixin(GenericAPIView):

    def get_serializer(self, *args, **kwargs):
        refresh_token = self.request.COOKIES.get('refresh_token', None)
        if refresh_token is not None:
            kwargs['data'] = {
                'refresh': refresh_token,
                **kwargs.get('data', {})
            }
        return super().get_serializer(*args, **kwargs)


@extend_schema(
    tags=["Authentification"],
    responses=UserTokensSerializer
)
class TokenObtainPairView(SetTokensInCookieMixin, jwt_views.TokenObtainPairView):
    pass


@extend_schema(
    tags=["Authentification"],
)
class TokenRefreshView(UserTokensInCookieMixin, SetTokensInCookieMixin, jwt_views.TokenRefreshView):
    pass


@extend_schema(
    tags=["Authentification"],
)
class LogoutView(UserTokensInCookieMixin, jwt_views.TokenBlacklistView):

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
        return super().finalize_response(request, response, *args, **kwargs)


@extend_schema(
    tags=["Authentification"],
    responses=UserTokensSerializer
)
class RegisterView(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        token = RefreshToken.for_user(instance)
        data = {
            'refresh': str(token),
            'access': str(token.access_token),
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)
