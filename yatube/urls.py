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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # flatpages
    path("about/", include("django.contrib.flatpages.urls")),

    # регистрация и авторизация
    path("auth/", include("users.urls")),

    # если нужного шаблона для /auth не нашлось в файле users.urls —
    # ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    # раздел администратора
    path("admin/", admin.site.urls),

    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='about-spec'),

    # обработчик для главной страницы ищем в urls.py приложения posts
    path("", include("posts.urls")),
]

# добавим новые пути
urlpatterns += [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)