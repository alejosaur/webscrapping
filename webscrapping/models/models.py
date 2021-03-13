from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.inspection import inspect
from app import db

class Product(db.Model):
    """Producto publicado por proveedor"""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    provider = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    #records = relationship("Record", backref="Product", lazy='dynamic')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "url": self.url,
                "provider": self.provider,
                "Record": [x.serialize() for x in self.Record]}

    def serializeSimple(self):
        return {"id": self.id,
                "name": self.name,
                "url": self.url,
                "provider": self.provider,
                "last_record": self.Record[-1].serialize()}


class Record(db.Model):
    """Registro de precio de un producto"""
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    base_price = Column(Float, nullable=False)
    discount = Column(String, nullable=False)
    discounted_price = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    ProductId = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product", backref="Record")

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
        
    def serialize(self):
        return {"id": self.id,
                "base_price": self.base_price,
                "discount": self.discount,
                "discounted_price": self.discounted_price,
                "date": self.date}

db.create_all()