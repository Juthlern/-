from sqlalchemy import create_engine
from main import Base, User, Address
from sqlalchemy.orm import sessionmaker
import uuid

engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/test_db',
    echo=True
)

print("🗑️Удаляем старые таблицы...")
Base.metadata.drop_all(engine)

print("🔄Создаем новые таблицы с UUID...")
Base.metadata.create_all(engine)

print("\n✅Таблицы пересозданы с правильной структурой!")
print("Теперь все id будут типа UUID")