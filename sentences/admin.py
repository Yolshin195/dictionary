from django.contrib import admin
from .models import Language
from .models import Word
from .models import Translate
from .models import Sentence
from .models import SentenceWord

admin.site.register(Language)
admin.site.register(Word)
admin.site.register(Translate)
admin.site.register(Sentence)
admin.site.register(SentenceWord)
