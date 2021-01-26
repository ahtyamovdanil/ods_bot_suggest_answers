

def prepare_response_text(prefix, suggestion):
    """
    Подготавливает текст ответа от имени бота.

    :param prefix:
        `str`, префикс, который будет указан перед ссылками на похожие треды.
    :param suggestion:
        `iter`, список ссылок на похожие тереды.

    :return:
        `str`, текст ответа.
    """
    text = [prefix]
    text.extend(suggestion)
    return '\n\n'.join(text)


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
