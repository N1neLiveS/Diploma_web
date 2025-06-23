from django import forms
from .models import Answer, Question


class TakeTestForm(forms.Form):
    def __init__(self, test, user, *args, **kwargs): # Add user as an argument
        super().__init__(*args, **kwargs)
        self.test = test
        self.user = user  # Save the user
        self.question_queryset = self.test.get_questions_for_user(self.user)  # Get the adapted questions
        # Динамическое создание полей для вопросов
        for question in self.question_queryset:
            choices = [(answer.id, answer.text) for answer in question.answers.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                label=question.text,
                widget=forms.RadioSelect  # Или другой виджет
            )

    def calculate_score(self, user):
        score = 0
        for question in self.test.questions.all():
            selected_answer_id = self.cleaned_data.get(f'question_{question.id}')
            if selected_answer_id:
                try:
                    answer = question.answers.get(id=selected_answer_id)
                    if answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass
        return score