# test_db.py

import psycopg2
from src.config.settings import settings

try:
    conn = psycopg2.connect(settings.pg_dsn)

    cur = conn.cursor()
    cur.execute("SELECT version();")

    print("✅ Connected successfully")
    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed")
    print(e)