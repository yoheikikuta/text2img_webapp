import numpy as np


def call_text2img(text: str) -> np.ndarray:
    """
    TODO: Replace this method with treating gerenerated images.
    """
    import requests

    response = requests.get("http://backend:80", params={"text": text})

    return np.frombuffer(response.content, dtype='uint8').reshape(256,256*5,3)


def translate_text(target: str, src_text: str) -> str:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(src_text, six.binary_type):
        src_text = src_text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(src_text, target_language=target)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]
