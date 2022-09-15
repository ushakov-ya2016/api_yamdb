from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Проверяет, чтобы год выпуска не был больше текущего.
    """
    if value > datetime.now().year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего.',
            params={'value': value},
        )


def validate_score(value):
    """
    Проверяет, чтобы оценка произведения была от 1 до 10.
    """
    if value < 1 or value > 10:
        raise ValidationError(
            'Оценка произведения должны быть от 1 до 10',
            params={'value': value},
        )
