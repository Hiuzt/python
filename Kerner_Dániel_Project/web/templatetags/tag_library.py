from django import template

register = template.Library()


@register.filter()
def invoice_type(value):
    types = ["Normál", "Egy tekintet", "Proforma", "Egyéb", "Másolat", "Módosító"]
    return types[int(value) - 1]

@register.filter()
def e_invoice(value):
    types = ["E-számla", "Papír számla"]
    return types[int(value) - 1] 
