import django_filters
from .models import BlogPost

class BlogPostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')

    class Meta:
        model = BlogPost
        fields = ['created_at']