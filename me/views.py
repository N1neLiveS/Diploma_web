from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from help.models import Question
from articles.models import Article
from .forms import EditProfileForm, EditProfileAvatarForm, PasswordChangingForm


@login_required
def me(request):
    user = request.user
    questions = Question.objects.filter(author=user).order_by('-created_at')
    articles = Article.objects.filter(author=user).order_by('-created_at')
    return render(request, 'me/me.html', {'questions': questions, 'articles': articles})


@login_required
def settings_account(request):
    user = request.user
    profile = user.profile  # Получаем профиль пользователя

    if request.method == 'POST':
        form_password = PasswordChangingForm(user=request.user, data=request.POST)
        if form_password.is_valid():
            form_password.save()
            update_session_auth_hash(request, form_password.user)  # Важно для сохранения сессии
            messages.success(request, 'Password changed successfully')
            return redirect('settings_account')  # Redirect на страницу профиля
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form_password = PasswordChangingForm(user=request.user)

    if request.method == 'POST':
        profile_form = EditProfileAvatarForm(request.POST, request.FILES, instance=profile)
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('settings_account')  # Redirect на эту же страницу
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=user)
        profile_form = EditProfileAvatarForm(instance=profile) # Инициализация формы профиля

    return render(request, 'me/settings.html', {
        'form': form,
        'profile_form': profile_form,
        'form_password': form_password,
    })

