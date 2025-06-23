import math
from django.db.models import Avg


def calculate_user_level(user, tags):
    """
    Вычисляет уровень пользователя по заданным тегам
    на основе его профиля и предыдущих попыток
    """
    profile = user.profile
    topic_scores = profile.get_python_topic_scores()

    # Получаем средний балл по запрошенным тегам
    relevant_scores = []
    for tag in tags:
        tag_name = tag.name if hasattr(tag, 'name') else str(tag)
        if tag_name in topic_scores:
            relevant_scores.append(topic_scores[tag_name])

    if not relevant_scores:
        return 50  # Средний уровень по умолчанию

    return sum(relevant_scores) / len(relevant_scores)


def update_user_skills(user, question, is_correct):
    """
    Обновляет навыки пользователя после ответа на вопрос
    """
    profile = user.profile
    topic_scores = profile.get_python_topic_scores()

    # Параметры IRT модели
    DISCRIMINATION = 1.0
    GUESSING = 0.25

    difficulty = question.difficulty
    reward = question.reward

    for tag in question.tags.names():
        user_ability = topic_scores.get(tag, 50)  # Начальный уровень 50

        # Рассчитываем IRT-балл
        if is_correct:
            probability = GUESSING + (1 - GUESSING) / (
                    1 + math.exp(-DISCRIMINATION * (user_ability - difficulty)))
            score_change = reward * probability
        else:
            probability = 1 - (GUESSING + (1 - GUESSING) / (
                    1 + math.exp(-DISCRIMINATION * (user_ability - difficulty))))
            score_change = -reward * probability * 0.5  # Штраф за неправильный ответ

        # Обновляем уровень с плавным усреднением
        if tag in topic_scores:
            topic_scores[tag] = max(0, min(100,
                                           0.7 * topic_scores[tag] + 0.3 * (user_ability + score_change)))
        else:
            topic_scores[tag] = max(0, min(100, 50 + score_change))

        profile.update_python_topic_scores(topic_scores)
