"""
データベースマイグレーション実行スクリプト

token_usageテーブルを作成するためのマイグレーションを実行します。
"""

import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()


def run_migration():
    """マイグレーションを実行"""
    # データベース接続情報を環境変数から取得
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ エラー: DATABASE_URLが設定されていません")
        print("   .envファイルにDATABASE_URLを設定してください")
        sys.exit(1)

    # PostgreSQL接続URLをpsycopg2形式にパース
    # 例: postgresql://user:password@localhost:5432/dbname
    try:
        if database_url.startswith("postgresql://"):
            # postgresql:// を除去
            url_parts = database_url.replace("postgresql://", "")
            # user:password@host:port/dbname を分解
            auth_host = url_parts.split("@")
            user_pass = auth_host[0].split(":")
            host_port_db = auth_host[1].split("/")
            host_port = host_port_db[0].split(":")

            user = user_pass[0]
            password = user_pass[1]
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else "5432"
            database = host_port_db[1]
        else:
            print(f"❌ エラー: 不正なDATABASE_URL形式: {database_url}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ エラー: DATABASE_URLのパースに失敗しました: {e}")
        sys.exit(1)

    # マイグレーションSQLファイルのパス
    migrations_dir = Path(__file__).parent.parent / "migrations"
    migration_files = [
        "001_create_token_usage_table.sql",
        "002_add_conversation_columns.sql"
    ]

    # PostgreSQLに接続
    try:
        print("📊 データベースに接続中...")
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        cursor = conn.cursor()

        # 各マイグレーションファイルを順番に実行
        for migration_filename in migration_files:
            migration_file = migrations_dir / migration_filename

            if not migration_file.exists():
                print(f"⚠ 警告: マイグレーションファイルが見つかりません: {migration_filename}")
                continue

            # マイグレーションSQLを読み込む
            with open(migration_file, "r", encoding="utf-8") as f:
                migration_sql = f.read()

            print(f"🔄 マイグレーションを実行中: {migration_filename}")
            cursor.execute(migration_sql)
            conn.commit()
            print(f"✅ {migration_filename} が正常に完了しました")

        print("\n✅ 全てのマイグレーションが正常に完了しました")
        print("   テーブル 'token_usage' が作成・更新されました")

        # テーブルが作成されたことを確認
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'token_usage'
        """
        )
        result = cursor.fetchone()

        if result:
            print(f"   ✓ テーブル確認: {result[0]}")
        else:
            print("   ⚠ 警告: テーブルが見つかりませんでした")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"❌ データベースエラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("  トークン使用量テーブル マイグレーション")
    print("=" * 60)
    print()
    run_migration()
    print()
    print("=" * 60)
    print("  マイグレーション完了")
    print("=" * 60)
