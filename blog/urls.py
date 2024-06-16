from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import (BlogPostCreateView, BlogPostListView, BlogPostDetailView,
                        BlogPostUpdateView, BlogPostDeleteView, toggle_publication)

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('', BlogPostListView.as_view(), name='list'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='update'),
    path('<int:pk>/view/', cache_page(60)(BlogPostDetailView.as_view()), name='view'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='delete'),
    path('<int:pk>/publication/', toggle_publication, name='toggle_publication'),
]
