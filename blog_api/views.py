from graphene_django.views import GraphQLView
from django.http import JsonResponse

class PrivateGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You must be logged in to access this endpoint.'}, status=403)
        return super().dispatch(request, *args, **kwargs)
