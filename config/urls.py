from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('mailing.urls', 'mailing'))),
    path('client/', include(('client.urls', 'client'))),
    path('users/', include(('users.urls', 'users'))),
    path('blog/', include(('blog.urls', 'blog'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
