import psycopg2


def get_db_connection():

    # Database connection parameters
    host = "localhost"         # or your DB server IP
    port = "5432"              # default PostgreSQL port
    dbname = "LostnFound-db"   # replace with your database name
    user = "postgres"     # replace with your username
    password = "Nagashree@postgres" # replace with your password

    try:
        # Establish connection
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        print("✅ Connected to the database successfully!")

        # # Create a cursor object
        # cur = conn.cursor()

        # # Example query
        # cur.execute("SELECT version();")
        # db_version = cur.fetchone()
        # print("Database version:", db_version)
        return conn

        # Close cursor and connection
        # cur.close()
        # conn.close()

    except Exception as e:
        print("❌ Failed to connect to the database.")
        print("Error:", e)
