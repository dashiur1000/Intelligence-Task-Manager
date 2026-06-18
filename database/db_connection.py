import mysql.connector

class DB_connection:

    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "1234"
        self.database = "Intelligence_db"

    def get_connections(self):
        conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        return conn



    def create_database(self):
        conn = mysql.connector.connect(host= self.host, user= self.user, password= self.password)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        cursor.close()
        conn.close()


    def create_tables(self):
        conn = self.get_connections()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS agents(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            specialty VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            completed_missions INT DEFAULT 0,
            failed_missions INT DEFAULT 0,
            agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL)
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS missions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(100) NOT NULL,
            difficulty INT CHECK(difficulty BETWEEN 1 AND 10) NOT NULL,
            importance INT CHECK(importance BETWEEN 1 AND 10) NOT NULL,
            status ENUM('NEW', 'ASSIGNED', 'PROGRESS_IN', 'COMPLETED', 'FAILED', 'CANCELLED'),
            risk_level VARCHAR(100),
            assigned_agent_id INT DEFAULT NULL
            )""")
        conn.commit()
        cursor.close()
        conn.close()

# db = DB_connection()

# if __name__ == "__main__":
#     db.create_database()
#     db.create_tables()