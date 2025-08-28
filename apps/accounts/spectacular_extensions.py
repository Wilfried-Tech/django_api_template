from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTAndCookieAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'apps.accounts.authentication.JWTAndCookieAuthentication'
    name = 'JWTAndCookieAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access_token',
        }
