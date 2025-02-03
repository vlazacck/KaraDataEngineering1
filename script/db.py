import psycopg2
from psycopg2 import sql, OperationalError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="db.log"
)

class Database:
    def __init__(self, dbname, user, password, host, port):
        """
        Initialize the database connection parameters.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connect to the PostgreSQL database.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            logging.info("Connected to the database successfully.")
        except OperationalError as e:
            logging.error(f"Database connection error: {e}")
            raise

    def close(self):
        """
        Close the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logging.info("Database connection closed.")

    def execute_query(self, query, params=None):
        """
        Execute a SQL query with optional parameters.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            logging.info(f"Query executed: {query}")
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise

    def fetch_all(self):
        """
        Fetch all rows from the last executed query.
        """
        try:
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching results: {e}")
            raise

    def commit(self):
        """
        Commit the current transaction.
        """
        try:
            self.conn.commit()
            logging.info("Transaction committed.")
        except Exception as e:
            logging.error(f"Error committing transaction: {e}")
            raise

    def create_table(self, table_name, columns):
        """
        Create a table with the specified columns.
        Args:
            table_name (str): Name of the table.
            columns (list): List of column definitions (e.g., ["id SERIAL PRIMARY KEY", "name TEXT"]).
        """
        try:
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.SQL, columns))
            )
            self.execute_query(query)
            logging.info(f"Table '{table_name}' created successfully.")
        except Exception as e:
            logging.error(f"Error creating table '{table_name}': {e}")
            raise

    def insert_data(self, table_name, data):
        """
        Insert data into a table.
        Args:
            table_name (str): Name of the table.
            data (list): List of dictionaries where each dictionary represents a row to insert.
        """
        try:
            # Dynamically construct the INSERT query
            columns = data[0].keys()
            placeholders = ", ".join(["%s"] * len(columns))
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(placeholders)
            )

            # Insert each row
            for row in data:
                self.execute_query(query, tuple(row[col] for col in columns))
            self.commit()
            logging.info(f"Data inserted into table '{table_name}' successfully.")
        except Exception as e:
            logging.error(f"Error inserting data into table '{table_name}': {e}")
            raise

    def list_tables(self):
        """
        List all tables in the 'public' schema.
        """
        try:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            self.execute_query(query)
            tables = self.fetch_all()
            logging.info("Tables listed successfully.")
            return tables
        except Exception as e:
            logging.error(f"Error listing tables: {e}")
            raise


# Example usage
if __name__ == "__main__":
    # Initialize the database connection
    db = Database(
        dbname="ethiopian_medical_data",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    try:
        # Connect to the database
        db.connect()

        # List tables in the database
        tables = db.list_tables()
        print("Tables in the database:", tables)

        # Create a new table (example)
        table_name = "object_detections"
        columns = [
            "id SERIAL PRIMARY KEY",
            "file_name TEXT NOT NULL",
            "class_id INTEGER NOT NULL",
            "x_center FLOAT NOT NULL",
            "y_center FLOAT NOT NULL",
            "width FLOAT NOT NULL",
            "height FLOAT NOT NULL",
            "confidence FLOAT",
            "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]
        db.create_table(table_name, columns)

        # Insert data into the table (example)
        data = [
            {"file_name": "13", "class_id": 41, "x_center": 0.631250, "y_center": 0.515625, "width": 0.053125, "height": 0.056250, "confidence": 0.95},
            {"file_name": "13", "class_id": 32, "x_center": 0.504297, "y_center": 0.502734, "width": 0.089844, "height": 0.092969, "confidence": 0.85}
        ]
        db.insert_data(table_name, data)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        db.close()