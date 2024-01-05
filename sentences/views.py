from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import WordForm, SentenceForm
from .models import Word, Sentence


def home_page(request):
    return render(request, "sentences/home.html")


def word_list(request):
    search_text = request.POST.get("search_text", "")
    page_num = request.GET.get("page", 1)
    size = request.GET.get("size", 5)
    words = Word.search(search_text)
    paginator = Paginator(words, size)
    page = paginator.page(page_num)
    context = {"search_text": search_text, "words": words, "page": page}
    return render(request, "sentences/word_list.html", context)


def word_detail(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    translations = word.translate_set.all()

    sentences = [
        {"index": index, "id": sentence_id, "value": sentence_value}
        for index, sentence_id, sentence_value in word.sentenceword_set.values_list(
            "index", "sentence__id", "sentence__value"
        )
    ]
    print(sentences)
    context = {"word": word, "translations": translations, "sentences": sentences}
    return render(request, "sentences/word_detail.html", context)


def add_word(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("word_list")  # Перенаправление на страницу со списком слов
    else:
        form = WordForm()

    return render(request, "sentences/add_word.html", {"form": form})


def sentence_list(request):
    search_text = request.POST.get("search_text", "")
    sentences = Sentence.search(search_text)
    context = {"search_text": search_text, "sentences": sentences}
    return render(request, "sentences/sentence_list.html", context)


def sentence_detail(request, sentence_id):
    sentence = get_object_or_404(Sentence, id=sentence_id)
    words = [
        {"index": index, "id": word_id, "name": word_name}
        for index, word_id, word_name in sentence.sentenceword_set.values_list(
            "index", "word__id", "word__name"
        )
    ]
    context = {"sentence": sentence, "words": words}
    return render(request, "sentences/sentence_detail.html", context)


def add_sentence(request):
    if request.method == "POST":
        form = SentenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sentence_list")
    else:
        form = SentenceForm()

    return render(request, "sentences/add_sentence.html", {"form": form})
