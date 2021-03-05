from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app import db

class Product(db.Model):
    """Categorías de los artículos"""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    records = relationship("Record", backref="Product", lazy='dynamic')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


class Record(db.Model):
    """Artículos de nuestra tienda"""
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    base_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=False)
    ProductId = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product", backref="Record")

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
