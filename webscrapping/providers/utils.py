    from re import sub
from decimal import Decimal
from datetime import date
from sqlalchemy.orm.exc import NoResultFound

def calculate_discount(old, discounted):
    print(old, discounted)

    discounted_float = Decimal(sub(r'[^\d,]', '', discounted))
    old_float = Decimal(sub(r'[^\d,]', '', old))
    discount = 100-(discounted_float * 100 / old_float)
    return round(discount, 2)

def save(url, provider, name, price, discounted, discount):
    from webscrapping.models.models import Product, Record
    from app import db
    
    product = None
    try:
        product = Product.query.filter_by(url=url).one()
    except NoResultFound:
        product = Product(name=name, provider=provider, url=url)
        db.session.add(product)
        db.session.commit()

    record = None
    try:
        record = Record.query.filter_by(product=product, date=date.today().strftime("%d/%m/%Y")).one()
    except NoResultFound:
        record = Record(base_price=price.replace('.',''), discount = discount, discounted_price = discounted.replace('.',''), date=date.today().strftime("%d/%m/%Y"), product = product)
        db.session.add(record)
        db.session.commit()