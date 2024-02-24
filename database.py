import psycopg2


def db_connection():
    db_con = psycopg2.connect(
        database='pharmacydb',
        user='postgres',
        password='Sabirova@447',
        host='localhost',
        port=5432
    )

    return db_con
