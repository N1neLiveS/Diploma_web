from django.contrib import admin
from .models import Test, Question, Answer, UserTestAttempt

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserTestAttempt)
