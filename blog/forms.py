from django import forms

from blog.models import BlogPost
from users.forms import StileFormMixin


class BlogPostForm(StileFormMixin, forms.ModelForm):
    """Форма для создания статьи"""
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'image',)