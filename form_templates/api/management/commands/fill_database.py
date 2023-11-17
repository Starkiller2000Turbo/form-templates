from datetime import datetime
from logging import getLogger
from random import randrange, sample
from string import ascii_letters as letters
from string import digits
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from tinydb import TinyDB

logger = getLogger(__name__)


class Command(BaseCommand):
    """Команда для импорта записей из файла."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Функция для импорта записей из файла."""
        db = TinyDB(settings.DATA_STORAGE_LOCATION)
        logger.info(
            'Successfully connected to database in: '
            f'{settings.DATA_STORAGE_LOCATION}',
        )
        db.truncate()
        logger.info('Successfully cleared database')
        logger.info('Inserting data')
        counter = 0
        for i in range(settings.DATABASE_VARIABILITY):
            db.insert(
                {
                    'name': ''.join(
                        sample(letters, k=settings.NAMES_LENGTH),
                    ),
                    'user_phone': (
                        f"+7 {''.join(sample(digits, k=3))} "
                        f"{''.join(sample(digits, k=3))} "
                        f"{''.join(sample(digits, k=2))} "
                        f"{''.join(sample(digits, k=2))}"
                    ),
                    'lead_email': (
                        f"{''.join(sample(letters, k=settings.EMAIL_LENGTH))}"
                        '@mail.ru'
                    ),
                    'order_date': datetime(
                        year=randrange(2023),
                        month=randrange(1, 12),
                        day=randrange(1, 29),
                    ).strftime('%d.%m.%Y'),
                    'message_text': ''.join(
                        sample(
                            letters,
                            k=settings.TEXT_LENGTH,
                        ),
                    ),
                },
            )
            counter += 1
        logger.info(f'Created {counter} ')
