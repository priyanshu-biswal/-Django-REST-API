from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import IsOwner
from .filters import BlogPostFilter

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        # Restrict users to only access their own posts
        return BlogPost.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Set author to current logged-in user automatically
        serializer.save(author=self.request.user)