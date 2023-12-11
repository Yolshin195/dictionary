from django.urls import path

from .views import home_page, add_word, add_sentence
from .views import sentence_list
from .views import sentence_detail
from .views import word_list
from .views import word_detail

urlpatterns = [
    path('', home_page, name="home_page"),
    path('sentence/', sentence_list, name="sentence_list"),
    path('sentence/add/', add_sentence, name="add_sentence"),
    path('sentence/detail/<str:sentence_id>', sentence_detail, name="sentence_detail"),
    path('word/', word_list, name="word_list"),
    path('word/add/', add_word, name="add_word"),
    path('word/detail/<str:word_id>', word_detail, name="word_detail"),
]
