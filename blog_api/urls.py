from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the API, Go to '/graphql' for access interface ")

urlpatterns = [
    path('', home),  # This will handle requests to the root URL /
    path('admin/', admin.site.urls),  # Admin panel URL
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]
