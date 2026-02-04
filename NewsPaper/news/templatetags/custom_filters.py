from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
BAD_WORDS = {'редиска', 'дурак', 'идиот', 'простофиля', 'глупец', 'тупой'}


@register.filter
def hide_forbidden(value):
    def censor_word(word):
        clean = word.rstrip('.,!?;:"()[]{}')
        punct = word[len(clean):]
        if clean.lower() in BAD_WORDS:
            if len(clean) <= 2:
                return "*" * len(clean) + punct
            return clean[0] + "*" * (len(clean) - 2) + clean[-1] + punct
        return word

    return " ".join(censor_word(w) for w in value.split())

