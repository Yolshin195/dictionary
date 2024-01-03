from django import forms
from django.db import transaction

from .models import Word, Sentence, SentenceWord
from .services.sentence_splitter import sentence_split
from .tasks import ru_translate


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['name', 'code', 'language']

    def __init__(self, *args, **kwargs):
        super(WordForm, self).__init__(*args, **kwargs)
        # Добавим атрибуты и стили, если нужно
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter word name'})
        self.fields['code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter word code'})
        self.fields['language'].widget.attrs.update({'class': 'form-control'})


class SentenceForm(forms.ModelForm):

    class Meta:
        model = Sentence
        fields = ['language', 'value']

    def __init__(self, *args, **kwargs):
        super(SentenceForm, self).__init__(*args, **kwargs)
        # Add attributes and styles if needed
        self.fields['language'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'rows': 4, 'placeholder': 'Enter sentence'})

    def save(self, commit=True):
        sentence = super().save(commit=False)

        if commit is False:
            return sentence

        words = sentence_split(self.cleaned_data['value'])

        with transaction.atomic():
            sentence.save()

            for index, word_text in enumerate(words):
                language = self.cleaned_data['language']
                word, created = Word.objects.get_or_create(code=word_text.upper(), name=word_text, language=language)

                if created:
                    ru_translate.delay(word.id)

                SentenceWord.objects.create(
                    word=word,
                    sentence=sentence,
                    index=index
                )

        return sentence
