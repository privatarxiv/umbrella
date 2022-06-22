"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Регистрация и авторизация
    path("auth/", include("users.urls")),
    # Если нужного шаблона для /auth не нашлось в файле users.urls — ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    # Раздел администратора
    path("adminka/", admin.site.urls),

    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),

    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='spec'),

    # Импорт url-ов из приложения api
    path('api/v1/', include('api.urls')),
    # Документация API
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),

    # Импорт url-ов из приложения posts
    path("", include("posts.urls")),
]

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa


# Мы добавляем возможность загрузки файлов пользователями, а значит, эти файлы должны быть доступны
# для просмотра в режиме разработки. Этот код будет работать, когда ваш сайт в режиме отладки.
# Он позволяет обращаться файлам в директории, указанной в MEDIA_ROOT по имени, через префикс MEDIA_URL.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
