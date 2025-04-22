from django.utils import timezone
from .models import EventUser, EventLog
from django.template.loader import render_to_string
import json


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
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if EventLog.objects.filter(user=request.user, timestamp__gte=today_start).exists():
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

        event = EventUser.objects.filter(start_date__lte=now, end_date__gte=now, tags__name=least_learned_topic_lower).order_by('priority').first()
        if not event:
            print('нет ивента')
            return None

        content_object = event.content_object
        content_type = event.content_type.model
        print(f"Content type: {content_type}")

        context = {'content_object': content_object, 'content_type': content_type, 'topic': least_learned_topic}

        event_html = render_to_string(event.template_name, context, request=request)
        # EventLog.objects.create(user=request.user, event=event)

        return event_html