from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from helloworld.views import BlogPostViewSet

router = DefaultRouter()
router.register('posts', BlogPostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', obtain_auth_token, name='api-token-auth'),
    path('api/', include(router.urls)),
]