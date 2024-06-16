from django import forms

from blog.models import BlogPost
from users.forms import StileFormMixin


class BlogPostForm(StileFormMixin, forms.ModelForm):
    """Форма для создания статьи"""
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'image',)


class BlogPostModeratorForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('published',)
