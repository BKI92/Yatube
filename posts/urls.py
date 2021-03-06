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
from django.urls import path
from . import views

urlpatterns = [
    path("<username>/<int:post_id>/comment/", views.add_comment,
         name="add_comment"),
    path("new/", views.new_post, name="new"),
    path("group/<slug:slug>/", views.group_posts, name='group'),

    path("follow/", views.follow_index, name="follow_index"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"),
    path("<username>/unfollow/", views.profile_unfollow,
         name="profile_unfollow"),

    # Профайл пользователя
    path("<username>/", views.profile, name="profile"),

    # Просмотр записи
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("<username>/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("", views.index, name="index"),

]


