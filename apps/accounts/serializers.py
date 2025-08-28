import secrets
from base64 import b64encode, b64decode
from datetime import timedelta

from django.core import signing
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utils import htmltotext
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'is_superuser', 'password')
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_active', 'is_staff']


class CreateUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        exclude = ('groups', 'user_permissions', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class WithUserTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['data'] = UserSerializer(self.user).data
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirmation = serializers.CharField(write_only=True, min_length=8)
    message = serializers.CharField(read_only=True)

    def validate_old_password(self, value):
        if self.context['request'].user.is_staff:
            return value

        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(_("Le mot de passe actuel est incorrect."))
        return value

    def validate_new_password(self, value):
        if self.context['request'].user.check_password(value):
            raise serializers.ValidationError(_("Le nouveau mot de passe doit être différent de l'ancien."))
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise serializers.ValidationError(_("Les deux mots de passe ne correspondent pas."))
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])

    @property
    def data(self):
        return {'message': _('Mot de passe changé')}


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    token = serializers.CharField(read_only=True)
    verification_code = serializers.CharField(read_only=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Il n'existe pas d'utilisateur avec cet email."))

        if not user.is_active:
            raise serializers.ValidationError(_("Cet utilisateur est désactivé."))

        return value

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.get(email=email)
        verification_code = ''.join(list(map(lambda _: str(secrets.randbelow(10)), range(6))))

        html_content = render_to_string('auth/password_reset_email.html', {'verification_code': verification_code})
        text_content = htmltotext(html_content)
        user.email_user(
            subject=_("Réinitialisation de mot de passe"),
            message=text_content,
            from_email="security@example.com",
            html_message=html_content,
        )

        attrs['verification_code'] = verification_code
        attrs['token'] = signing.dumps({
            'uid': b64encode(force_bytes(user.pk)),
            'verification_code': verification_code
        })
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True, min_length=8)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(_("Les deux mots de passe ne correspondent pas."))

        try:
            token_data = signing.loads(attrs['token'], max_age=timedelta(minutes=3))
            uid = token_data['uid']

            if attrs['verification_code'] != token_data['verification_code']:
                raise serializers.ValidationError(_("Le code de vérification est incorrect."))

            user_id = force_str(b64decode(uid))
            user = User.objects.filter(pk=user_id).first()

            if not user:
                raise serializers.ValidationError(_("L'utilisateur n'existe pas."))

            if not user.is_active:
                raise serializers.ValidationError(_("Cet utilisateur est désactivé."))

        except (signing.BadSignature, signing.SignatureExpired, TypeError, ValueError, OverflowError):
            raise serializers.ValidationError(_("Le token est expiré ou invalide."))

        return attrs

    def data(self):
        return {'message': _('Mot de passe réinitialisé')}


UserTokensSerializer = inline_serializer(
    name='UserTokensSerializer',
    fields={
        'access': serializers.CharField(),
        'refresh': serializers.CharField(),
        'data': UserSerializer(),
    }
)

UserRefreshTokenSerializer = inline_serializer(
    name='UserRefreshTokenSerializer',
    fields={
        'refresh': serializers.CharField(required=False),
    }
)
