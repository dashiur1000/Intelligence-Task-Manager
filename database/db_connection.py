import mysql.connector

class DB_connection:

    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "1234"
        self.database = "intelligence-mysql"

    def get_connection(self):
        config = {"host": "localhost",
                  "port": 3306,
                  "user": "root",
                  "password": "1234",
                  "database": "intelligence-mysql"}
        conn = mysql.connector.connect(**config)
        return conn


    def create_database(self):
        config = {"host": self.host,
                  "user": self.user,
                  "password": self.password}
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")


    def create_tables(self):
        conn = self.get_connection()
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
        conn.commit()
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
            level_risk VARCHAR(100),
            assigned_agent_id INT DEFAULT NULL
            )""")
        conn.commit()
        cursor.close()
        conn.close()

db = DB_connection()
db.get_connection()

if __name__ == "__main__":
    db.get_connection()
    db.create_database()