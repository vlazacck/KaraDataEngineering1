
import psycopg2

# Database connection parameters
conn = psycopg2.connect(
    dbname="ethiopian_medical_data",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Test the connection
try:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)
except Exception as e:
    print("Error:", e)
finally:
    cursor.close()
    conn.close()

import psycopg2

# Database connection parameters
conn = psycopg2.connect(
    dbname="ethiopian_medical_data",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
