from celery import shared_task
from django.db import transaction

from sentences.models import Word, Translate, Language
from sentences.services.parse_word import parse_word


@shared_task
def ru_translate(word_id: str):
    word = Word.objects.get(id=word_id)
    ru_language = Language.objects.get(code="ru")

    if not word or not ru_language:
        return

    parse_result = parse_word(word.name)

    with transaction.atomic():
        word.description = parse_result.description
        word.save()

        translate = Translate(
            language=ru_language,
            word=word,
            value=parse_result.translate
        )
        translate.save()
