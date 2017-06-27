"""
Tests for transactional database operations
"""


def test_db_tables_created(db_inspector, db_tables, alembic_tables):
    # inspect db created for tables
    table_list = db_inspector.get_table_names()
    print(table_list)
    print(db_tables)

    assert table_list == alembic_tables + db_tables


