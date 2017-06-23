"""
Tests for transactional database operations
"""


from dbutils import DbConnection


def test_db_created(alchemy_url, db_setup):
    # confirm connection can be made to db created

    conn = DbConnection(alchemy_url)
    assert conn is not None


