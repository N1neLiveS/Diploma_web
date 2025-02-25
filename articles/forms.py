from django import forms
from .models import Article, ArticleComment
import bleach


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'poster']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

            self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
            self.fields['content'].required = False

        def clean_content(self):
            content = self.cleaned_data['content']
            # Очищаем HTML от потенциально опасных тегов и атрибутов
            cleaned_content = bleach.clean(content, tags=['p', 'img', 'figure', 'h1', 'h2', 'h3', 'a'],
                                           attributes={'img': ['src', 'alt', 'style', 'width', 'height']})
            return cleaned_content


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш комментарий'}),
        }