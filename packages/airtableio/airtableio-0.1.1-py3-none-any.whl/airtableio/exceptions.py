import time

_PREFIXES = ["error: ", "[error]: ", "bad request: ", "conflict: ", "not found: "]


def _clean_message(text):
    for prefix in _PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix) :]
    return (text[0].upper() + text[1:]).strip()


class AirtableAPIError(Exception):
    def __init__(self, message=None):
        super(AirtableAPIError, self).__init__(_clean_message(message))
