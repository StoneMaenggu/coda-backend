from sqlalchemy import create_engine

from api.models.tables import Base

DB_URL = "mysql+pymysql://root@db:3306/codadb?charset=utf8mb4"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    reset_database()