from sqlalchemy.exc import InternalError, OperationalError
from sqlalchemy import create_engine, text

from api.models.tables import Base
from api.db import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"
CODA_DB_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/codadb?charset=utf8mb4"
)

engine = create_engine(CODA_DB_URL, echo=True)

def database_exists():
    # 접속을 시도하여 coda 데이터베이스의 존재 확인
    try:
        engine.connect()
        return True
    except (OperationalError, InternalError) as e:
        print(e)
        print("database does not exist")
        return False

def create_database():
    if not database_exists():
        # demo 데이터베이스가 존재하지 않으면 생성
        root = create_engine(DB_URL, echo=True)
        with root.connect() as conn:
            conn.execute(text("CREATE DATABASE codadb"))
        print("created database")

    # DB 모델을 바탕으로 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("created tables")


if __name__ == "__main__":
    create_database()