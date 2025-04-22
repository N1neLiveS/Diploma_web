from django.contrib import admin
from .models import Article, ArticleComment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'article_tags')


admin.site.register(ArticleComment)
