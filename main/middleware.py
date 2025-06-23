from django.utils import timezone
from .models import EventUser, EventLog
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import json
import random


class EventMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.event_html = self.get_relevant_event_html(request)
        response = self.get_response(request)
        return response

    def get_relevant_event_html(self, request):
        if not request.user.is_authenticated:
            return None

        now = timezone.now()
        hour_ago = now - timezone.timedelta(hours=1)
        if EventLog.objects.filter(user=request.user, timestamp__gte=hour_ago).exists():
            return None

        user_profile = request.user.profile
        user_topic_scores = user_profile.get_python_topic_scores()

        least_learned_topic = None
        least_learned_score = 101
        for topic, score in user_topic_scores.items():
            if score is not None and score < least_learned_score:
                least_learned_topic = topic
                least_learned_score = score

        if not least_learned_topic:
            return None

        least_learned_topic_lower = least_learned_topic.lower()

        content_object, content_type, template_name = self.get_algorithmic_event(request, least_learned_topic_lower)

        if not content_object:
            print("content_object")
            return None

        context = {'content_object': content_object, 'content_type': content_type, 'topic': least_learned_topic}

        event_html = render_to_string(template_name, context, request=request)
        EventLog.objects.create(user=request.user, content_type=content_type, object_id=content_object.id)
        return event_html

    def get_algorithmic_event(self, request, least_learned_topic_lower):
        Article = apps.get_model('articles', 'Article')
        Lecture = apps.get_model('quests', 'Lecture')

        available_articles = Article.objects.filter(article_tags__name=least_learned_topic_lower).exclude(id__in=self.get_excluded_ids(request, Article))
        available_lectures = Lecture.objects.filter(tags__name=least_learned_topic_lower).exclude(id__in=self.get_excluded_ids(request, Lecture))

        all_options = list(available_articles) + list(available_lectures)

        if not all_options:
            return None, None, None

        chosen_content = random.choice(all_options)

        if isinstance(chosen_content, Article):
            template_name = 'main/event.html'
            content_type = ContentType.objects.get_for_model(Article)
        elif isinstance(chosen_content, Lecture):
            template_name = 'main/event.html'
            content_type = ContentType.objects.get_for_model(Lecture)
        else:
            return None, None, None
        self.add_to_excluded(request, chosen_content)

        return chosen_content, content_type, template_name

    def get_excluded_ids(self, request, model_class):
        excluded_key = f'excluded_{model_class._meta.model_name}s'
        excluded_ids = request.session.get(excluded_key, [])
        return excluded_ids

    def add_to_excluded(self, request, content_object):
         model_name = content_object.__class__._meta.model_name
         excluded_key = f'excluded_{model_name}s'
         excluded_ids = request.session.get(excluded_key, [])
         excluded_ids.append(content_object.id)
         request.session[excluded_key] = excluded_ids
