from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, ReviewForm
from .models import Post, Comment, Review


def forum(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/forum_layout.html', {'posts': posts})


@login_required  # Только авторизованные пользователи могут создавать посты
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Устанавливаем автора поста
            post.save()
            return redirect('post_detail', post_id=post.id)  # Перенаправляем на страницу поста
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Получаем список просмотренных постов из сессии
    viewed_posts = request.session.get('viewed_posts', [])

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    # Если пост ещё не был просмотрен
    if post_id not in viewed_posts:
        post.increment_views()  # Увеличиваем счётчик просмотров
        viewed_posts.append(post_id)  # Добавляем пост в список просмотренных
        request.session['viewed_posts'] = viewed_posts  # Обновляем сессию

    return render(request, 'forum/post_detail.html', {'post': post, 'form': form})


def reviews_layout(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'forum/reviews_layout.html', {'reviews': reviews})


@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user  # Устанавливаем автора
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'forum/create_review.html', {'form': form})