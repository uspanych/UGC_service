SQL_CREATE_TABLE = """
    CREATE TABLE views (
    id IDENTITY,
    user_id INTEGER NOT NULL,
    movie_id VARCHAR(256) NOT NULL,
    viewed_frame INTEGER NOT NULL
    );
"""

SQL_CREATE_RECORD = """
INSERT INTO views (user_id, movie_id, viewed_frame)
{data};
"""
