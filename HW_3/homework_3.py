from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

engine = create_engine("sqlite:///:memory:")

Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10, 2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


Base.metadata.create_all(engine)
