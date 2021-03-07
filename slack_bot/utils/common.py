

def preprocess_message(text, stem, stop_words):
    """
    Выполняет прероцессинг текста сообщения:
        - приводит все слова к нижнему регистру;
        - выполняет лемматизацию теста;
        - отбрасывает стоп-слова и пунктуацию;
        - выбирает слова, которые содержат хотя бы один буквенный символ.

    :param text:
        `str`, текст статьи.
    :param stem:
        `pymystem3.Mystem`, экземпляр лемматизатора.
    :param stop_words:
        `iter`, список стоп-слов.

    :return:
        `list`, список обработанных и отфильтрованных слов сообщения.
    """
    return [
        word for word in stem.lemmatize(text.lower())
        if word.isalpha() and word not in stop_words
    ]
