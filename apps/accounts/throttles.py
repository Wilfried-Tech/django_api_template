from rest_framework.throttling import SimpleRateThrottle


class PasswordResetRateThrottle(SimpleRateThrottle):
    scope = 'password_reset'

    def get_cache_key(self, request, view):
        email = request.data.get('email', None)
        if not email:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': email.lower().strip()
        }


class PasswordResetIPThrottle(SimpleRateThrottle):
    scope = 'password_reset_ip'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
