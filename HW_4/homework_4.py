from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, create_engine, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


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


engine = create_engine("sqlite:///:memory:")

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


electronics = Category(name="Электроника", description="Гаджеты и устройства.")
books = Category(name="Книги", description="Печатные книги и электронные книги.")
clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([electronics, books, clothes])
session.commit()


products = [
    Product(
        name="Смартфон",
        price=299.99,
        in_stock=True,
        category_id=electronics.id,
    ),
    Product(
        name="Ноутбук",
        price=499.99,
        in_stock=True,
        category_id=electronics.id,
    ),
    Product(
        name="Научно-фантастический роман",
        price=15.99,
        in_stock=True,
        category_id=books.id,
    ),
    Product(
        name="Джинсы",
        price=40.50,
        in_stock=True,
        category_id=clothes.id,
    ),
    Product(
        name="Футболка",
        price=20.00,
        in_stock=True,
        category_id=clothes.id,
    ),
]

session.add_all(products)
session.commit()


print("Все категории и продукты:")

categories = session.query(Category).all()

for category in categories:
    print(f"\nКатегория: {category.name}")
    print(f"Описание: {category.description}")

    for product in category.products:
        print(f"- {product.name}: {product.price}")


print("\nОбновление цены товара:")

product = session.query(Product).filter(Product.name == "Смартфон").first()

if product:
    product.price = 349.99
    session.commit()
    print(f"Обновленный товар: {product.name}\nНовая цена: {product.price}")
else:
    print("Товар не найден.")


print("\nОбщее количество продуктов в каждой категории:")

category_counts = (
    session.query(
        Category.name,
        func.count(Product.id),
    )
    .join(Product)
    .group_by(Category.name)
    .all()
)

for category_name, product_count in category_counts:
    print(f"{category_name}: {product_count}")


print("\nКатегории, в которых более одного продукта:")

filtered_categories = (
    session.query(
        Category.name,
        func.count(Product.id).label("product_count"),
    )
    .join(Product)
    .group_by(Category.name)
    .having(func.count(Product.id) > 1)
    .all()
)

for category_name, product_count in filtered_categories:
    print(f"{category_name}: {product_count}")
