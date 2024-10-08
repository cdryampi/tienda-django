from django import template

register = template.Library()

@register.filter
def as_material(field):
    return field.as_widget(attrs={
        'class': 'validate',
        'placeholder': field.label
    })
