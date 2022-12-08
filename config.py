import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    port=54321,
    database="company_service",
    user="thanhpv",
    password="22121992"
    )


