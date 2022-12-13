import psycopg2

from config import settings

postgres_db = psycopg2.connect(
    host=settings.PG_HOST,
    port=settings.PG_PORT,
    database=settings.PG_DATABASE,
    user=settings.PG_USER,
    password=settings.PG_PASSWORD
)
