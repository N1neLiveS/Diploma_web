from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm
from .models import Article, ArticleComment


def articles_main(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'articles/articles_layout.html', {'articles': articles})


@login_required
def create_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', article_id=article.id)
    else:
        article_form = ArticleForm()
    return render(request, 'articles/create_article.html', {'article_form': article_form})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Получаем список просмотренных постов из сессии
    viewed_articles = request.session.get('viewed_articles', [])

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    # Если пост ещё не был просмотрен
    if article_id not in viewed_articles:
        article.increment_views()  # Увеличиваем счётчик просмотров
        viewed_articles.append(article_id)  # Добавляем пост в список просмотренных
        request.session['viewed_articles'] = viewed_articles  # Обновляем сессию

    return render(request, 'articles/article_detail.html', {'article': article, 'form': form})
