from django import forms
from .models import Answer


class TakeTestForm(forms.Form):
    def __init__(self, test, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test = test
        for question in test.questions.all():
            choices = [(answer.id, answer.text) for answer in question.answers.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
                required=True
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