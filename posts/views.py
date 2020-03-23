from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    # тут тело функции
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author).order_by("-pub_date")
    total_posts = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"posts": posts, "author": author,
                                            'total_posts': total_posts,
                                            'page': page,
                                            'paginator': paginator}
                  )


def post_view(request, username, post_id):
    # тут тело функции
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author)
    total_posts = posts.count()
    post = Post.objects.filter(author=author, id=post_id).first()

    return render(request, "post.html",
                  {'post': post, "author": author, 'total_posts': total_posts})


def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if post.author == request.user:
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('profile', username)
    else:
        form = PostForm(instance=post)
    return render(request, "new.html", {"form": form, "post": post})
