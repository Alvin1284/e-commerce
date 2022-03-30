from django import template

register = template.Library()


@register.filter(name='currency')
def currency(number):
    return "$" + str(number)


@register.filter(name='multiply')
def multiply(number1, number2):
    return number1 * number2