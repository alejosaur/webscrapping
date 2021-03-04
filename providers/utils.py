from re import sub
from decimal import Decimal

def calculate_discount(old, discounted):
    discounted_float = Decimal(sub(r'[^\d,]', '', discounted))
    old_float = Decimal(sub(r'[^\d,]', '', old))
    discount = 100-(discounted_float * 100 / old_float)
    return round(discount, 2)