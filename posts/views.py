from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Comment
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html",
                  {"group": group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
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
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    total_posts = Post.objects.filter(author=author).count()
    form = CommentForm()
    items = Comment.objects.filter(post=post).order_by("created")
    return render(request, "post.html",
                  {"post": post, "username": username,
                   "author": author, "total_posts": total_posts,
                   "form": form, "items": items})


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect("post", username=request.user.username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username,
                            post_id=post_id)

    return render(
        request, "new.html", {"form": form, "post": post},
    )


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
    return redirect('post', username, post_id)
