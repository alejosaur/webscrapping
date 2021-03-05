from re import sub
from decimal import Decimal

def calculate_discount(old, discounted):
    discounted_float = Decimal(sub(r'[^\d,]', '', discounted))
    old_float = Decimal(sub(r'[^\d,]', '', old))
    discount = 100-(discounted_float * 100 / old_float)
    return round(discount, 2)

def save(url, name, price, discounted, discount):
    from webscrapping.models.models import Product
    product = Product(nombre=name, url=url)
    db.session.add(product)
    db.session.commit()