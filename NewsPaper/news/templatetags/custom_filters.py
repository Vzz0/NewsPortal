from sys import prefix

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
BAD_WORDS = {'редиска', 'дурак', 'идиот', 'простофиля', 'глупец', 'тупой'}

@register.filter()
@stringfilter
def censor(value):
    if not isinstance(value, str):
        raise TypeError("Фильтр 'censor' может применяться только к строкам.")

    words = value.split()
    result = []

    for word in words:
        stripped = word.rstrip('.,!?;:"()[]{}')
        punctuation = word[len(stripped):]
        if stripped.lower() in BAD_WORDS:
            if stripped and stripped[0].isupper():
                censored = stripped[0] + '*' * (len(stripped) - 1)
            else:
                censored = '*' * len(stripped)
            result.append(censored + punctuation)
        else:
            result.append(word)

    return ' '.join(result)

