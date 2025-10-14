"""
トークン使用量のデータベースモデル

SQLAlchemyを使用してtoken_usageテーブルとPythonオブジェクトをマッピングします。
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemyのベースクラス
Base = declarative_base()


class TokenUsage(Base):
    """
    トークン使用量を記録するモデル

    各LLM呼び出しのトークン使用量を保存します。
    """

    __tablename__ = "token_usage"

    # 主キー（自動採番）
    id = Column(Integer, primary_key=True, autoincrement=True)

    # セッションID（ADKのsessionsテーブルと紐付け可能）
    session_id = Column(String(255), nullable=False, index=True)

    # エージェント名（どのエージェントがトークンを使用したか）
    agent_name = Column(String(100), nullable=False, index=True)

    # トークン使用時刻
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # 入力トークン数（プロンプト）
    input_tokens = Column(Integer, nullable=False, default=0)

    # 出力トークン数（応答）
    output_tokens = Column(Integer, nullable=False, default=0)

    # 合計トークン数
    total_tokens = Column(Integer, nullable=False, default=0)

    # 使用モデル名（例: gemini-2.0-flash）
    model_name = Column(String(100), nullable=True)

    # ユーザーID（オプション）
    user_id = Column(String(255), nullable=True, index=True)

    # 呼び出しID（ADKの invocation_id と紐付け可能）
    invocation_id = Column(String(255), nullable=True)

    # ユーザーの発話内容
    user_message = Column(String, nullable=True)

    # AIの応答内容
    ai_response = Column(String, nullable=True)

    def __repr__(self) -> str:
        """オブジェクトの文字列表現"""
        return (
            f"<TokenUsage(id={self.id}, "
            f"agent={self.agent_name}, "
            f"input={self.input_tokens}, "
            f"output={self.output_tokens}, "
            f"total={self.total_tokens})>"
        )


class TokenUsageRepository:
    """
    トークン使用量の保存・取得を行うリポジトリクラス

    データベース操作をカプセル化します。
    """

    def __init__(self, database_url: str):
        """
        リポジトリを初期化

        Args:
            database_url: PostgreSQL接続URL
                例: postgresql://adk_user:adk_password@localhost:5432/adk_sessions
        """
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def save_token_usage(
        self,
        session_id: str,
        agent_name: str,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
        model_name: Optional[str] = None,
        user_id: Optional[str] = None,
        invocation_id: Optional[str] = None,
        user_message: Optional[str] = None,
        ai_response: Optional[str] = None,
    ) -> TokenUsage:
        """
        トークン使用量をデータベースに保存

        Args:
            session_id: セッションID
            agent_name: エージェント名
            input_tokens: 入力トークン数
            output_tokens: 出力トークン数
            total_tokens: 合計トークン数
            model_name: モデル名（オプション）
            user_id: ユーザーID（オプション）
            invocation_id: 呼び出しID（オプション）
            user_message: ユーザーの発話内容（オプション）
            ai_response: AIの応答内容（オプション）

        Returns:
            保存されたTokenUsageオブジェクト
        """
        session = self.Session()
        try:
            token_usage = TokenUsage(
                session_id=session_id,
                agent_name=agent_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                model_name=model_name,
                user_id=user_id,
                invocation_id=invocation_id,
                user_message=user_message,
                ai_response=ai_response,
            )
            session.add(token_usage)
            session.commit()
            session.refresh(token_usage)
            return token_usage
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
