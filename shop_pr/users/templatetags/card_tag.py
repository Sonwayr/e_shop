from django import template

register = template.Library()


@register.filter
def mask_card_number(card_number):
    masked_card_number = '*' * (len(card_number) - 4) + card_number[-4:]
    return masked_card_number
