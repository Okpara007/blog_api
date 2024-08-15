from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication

class EnforceJWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/graphql'):
            # Only enforce JWT authentication for GraphQL requests
            jwt_authenticator = JWTAuthentication()
            try:
                user, _ = jwt_authenticator.authenticate(request)
                request.user = user
            except Exception:
                pass  # Handle authentication failure as anonymous user
