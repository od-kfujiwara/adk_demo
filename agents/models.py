"""
SQLAlchemyモデル定義
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKeyConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# データベース接続URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://adk_user:adk_password@localhost:5432/adk_sessions"
)

# エンジンとセッションの作成
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TokenUsage(Base):
    """トークン使用量を記録するモデル"""
    __tablename__ = 'token_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(128), nullable=False)
    app_name = Column(String(128), nullable=False)
    user_id = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=False)
    user_message = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    input_tokens = Column(Integer, nullable=True)
    thoughts_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)

    # 複合外部キー制約
    __table_args__ = (
        ForeignKeyConstraint(
            ['event_id', 'app_name', 'user_id', 'session_id'],
            ['events.id', 'events.app_name', 'events.user_id', 'events.session_id'],
            ondelete='CASCADE'
        ),
    )

    def __repr__(self):
        return f"<TokenUsage(event_id={self.event_id}, total_tokens={self.total_tokens})>"


def get_db_session():
    """データベースセッションを取得"""
    return SessionLocal()
