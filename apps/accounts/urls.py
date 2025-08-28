from django.urls import path, include

from config.router import AppRouter
from apps.accounts.views import PasswordResetView, PasswordResetConfirmView, TokenObtainPairView, \
    TokenRefreshView, LogoutView, AccountView, ChangePasswordView, RegisterView

router = AppRouter()

urlpatterns = [
    path('auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('register/', RegisterView.as_view(), name='register'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('forgot-password/', PasswordResetView.as_view(), name='password_reset'),
        path('reset-password/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('change-password/', ChangePasswordView.as_view(), name='change_password'),
        path('account/', AccountView.as_view(), name='account'),
        path('logout/', LogoutView.as_view(), name='logout'),
    ]), name='auth'),
]
