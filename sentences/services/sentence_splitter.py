import nltk

nltk.download('punkt')


def sentence_split(sentence: str) -> list[str]:
    return nltk.word_tokenize(sentence)
