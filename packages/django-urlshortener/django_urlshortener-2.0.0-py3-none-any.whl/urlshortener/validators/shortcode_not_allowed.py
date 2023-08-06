from django.core.exceptions import ValidationError


BLACK_LISTED_SHORTCODES = ['admin', 'kirrn', 'vinit']
BLACK_LISTED_DOMAINS = ['127.0.0.1', 'localhost', 'kirr', 'bit', 'tiny']


def shortcode_not_allowed(value):
    if value in BLACK_LISTED_SHORTCODES:
        raise ValidationError("This shortcode is not allowed, Try another one.")
    return value
