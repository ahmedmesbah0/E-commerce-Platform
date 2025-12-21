"""
Database utilities and helper functions.
Provides connection management, migrations, and common operations.
"""

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session
from .base import Base, engine, get_db
from typing import List, Dict, Any
import os


def create_all_tables():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")


def drop_all_tables():
    """Drop all tables - use with caution!"""
    confirm = input("⚠️  This will delete ALL tables. Type 'YES' to confirm: ")
    if confirm == 'YES':
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped.")
    else:
        print("❌ Operation cancelled.")


def get_table_names() -> List[str]:
    """Get list of all table names in the database."""
    inspector = inspect(engine)
    return inspector.get_table_names()


def get_table_info(table_name: str) -> Dict[str, Any]:
    """Get detailed information about a table."""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    foreign_keys = inspector.get_foreign_keys(table_name)
    indexes = inspector.get_indexes(table_name)
    
    return {
        'table_name': table_name,
        'columns': columns,
        'foreign_keys': foreign_keys,
        'indexes': indexes
    }


def test_connection() -> bool:
    """Test database connection."""
    try:
        db = get_db()
        result = db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def get_model_count(model_class) -> int:
    """Get count of records in a model."""
    db = get_db()
    try:
        count = db.query(model_class).count()
        return count
    finally:
        db.close()


def bulk_insert(model_class, data: List[Dict[str, Any]]):
    """Bulk insert records."""
    db = get_db()
    try:
        instances = [model_class(**item) for item in data]
        db.bulk_save_objects(instances)
        db.commit()
        print(f"✅ Inserted {len(data)} records into {model_class.__tablename__}")
    except Exception as e:
        db.rollback()
        print(f"❌ Bulk insert failed: {e}")
        raise
    finally:
        db.close()


def truncate_table(model_class):
    """Truncate a table (delete all records)."""
    db = get_db()
    try:
        db.query(model_class).delete()
        db.commit()
        print(f"✅ Truncated table {model_class.__tablename__}")
    except Exception as e:
        db.rollback()
        print(f"❌ Truncate failed: {e}")
        raise
    finally:
        db.close()


def export_schema_sql(output_file: str = "schema_export.sql"):
    """Export database schema to SQL file."""
    from sqlalchemy.schema import CreateTable
    
    with open(output_file, 'w') as f:
        for table in Base.metadata.sorted_tables:
            f.write(str(CreateTable(table).compile(engine)) + ";\n\n")
    
    print(f"✅ Schema exported to {output_file}")


if __name__ == "__main__":
    # Quick test script
    print("=== E-Commerce Platform Database Utilities ===\n")
    
    print("Testing connection...")
    test_connection()
    
    print("\nAvailable tables:")
    tables = get_table_names()
    for i, table in enumerate(tables, 1):
        print(f"  {i}. {table}")
    
    print(f"\nTotal tables: {len(tables)}")
