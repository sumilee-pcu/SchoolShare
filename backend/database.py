
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# SQLite 데이터베이스 설정
DATABASE_URL = "sqlite:///./schoolshare.db"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # check_same_thread는 SQLite에만 필요
)

# 데이터베이스 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """데이터베이스와 테이블을 생성합니다."""
    Base.metadata.create_all(bind=engine)
    print("데이터베이스와 테이블이 성공적으로 생성되었습니다.")
