from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship, selectinload
from sqlalchemy import String, ForeignKey, create_engine, select, Text
from uuid import UUID, uuid4
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=False)

    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    product_description: Mapped[str] = mapped_column(Text)
    product_price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")



engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/test_db',
    echo=True
)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session_factory = sessionmaker(engine)

def add_test_data():
    with session_factory() as session:
        
        users = [
            User(username="John Doe", email="jdoe@example.com", description="Постоянный клиент"),
            User(username="John Smith", email="jSmith@example.com", description="Новый клиент"),
            User(username="Alison Bree", email="Alison@example.com", description="VIP клиент"),
            User(username="Alfred Brown", email="ABrown@example.com", description="Корпоративный клиент"),
            User(username="Sam Winchester", email="SWin@example.com", description="Частый покупатель")
        ]
        session.add_all(users)
        session.commit()

        
        addresses = []
        for user in users:
            address = Address(
                user_id=user.id,
                street=f"456 {user.username.split()[0]} Avenue",
                city="Los Angeles",
                state="CA",
                zip_code="90001",
                country="USA",
                is_primary=True
            )
            addresses.append(address)
        session.add_all(addresses)
        session.commit()

        
        products_data = [
            {"name": "Игровая консоль", "description": "Последняя модель игровой консоли", "price": 499.99},
            {"name": "Камера", "description": "Профессиональная цифровая камера", "price": 1200.00},
            {"name": "Монитор", "description": "4K UHD монитор", "price": 350.00},
            {"name": "Клавиатура", "description": "Механическая клавиатура", "price": 150.00},
            {"name": "Мышь", "description": "Игровая мышь с подсветкой", "price": 80.00}
        ]

        orders = []

        for i, user in enumerate(users):
            product = products_data[i]
            order = Order(
                user_id=user.id,
                address_id=addresses[i].id,
                product_name=product["name"],
                product_description=product["description"],
                product_price=product["price"],
                quantity=2 + i,
                total_amount=product["price"] * (2 + i),
                status=["pending", "completed", "shipped", "processing", "delivered"][i]
            )
            orders.append(order)

        session.add_all(orders)
        session.commit()
        


add_test_data()