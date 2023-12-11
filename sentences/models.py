import uuid

from django.db import models


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} - {self.id}"


class BaseReference(BaseEntity):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name} ({self.code})"


class Language(BaseReference):
    pass


class Word(BaseReference):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    @classmethod
    def search(cls, search_text=None):
        if search_text:
            return cls.objects.filter(code__contains=search_text)

        return cls.objects.all()


class Translate(BaseEntity):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    value = models.CharField(max_length=128)


class Sentence(BaseEntity):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    value = models.TextField()

    @classmethod
    def search(cls, search_text=None):
        if search_text:
            return cls.objects.filter(value__contains=search_text)

        return cls.objects.all()


class SentenceWord(BaseEntity):
    index = models.IntegerField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.index is None:
            # Получаем максимальный индекс для данного предложения и добавляем 1
            max_index = SentenceWord.objects.filter(sentence=self.sentence).aggregate(models.Max('index'))['index__max']
            self.index = max_index + 1 if max_index is not None else 1
        super().save(*args, **kwargs)
