import mysql.connector

class DB_connection:

    def __init__(self, conn):
        self.conn = conn

    def get_connection(self, conn):
        conn = mysql.connector.connect(
        host = "localhost",
        password = "1234",
        database = "intelligence-mysql"
        )
        return conn


    def create_database(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE Intelligence_db IF NOT EXISTS")


    def create_tables(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE agents IF NOT EXISTS(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            specialty VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            completed_missions INT DEFAULT 0,
            failed_missions INT DEFAULT 0,
            agent_rank ENUM('Junior', 'Senior', 'Commander'))
            """
        )
        cursor.commit()
        cursor.execute(
            """
            CREATE TABLE missions IF NOT EXISTS(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT(100) NOT NULL,
            location VARCHAR(100) NOT NULL,
            difficulty INT(10) NOT NULL,
            importance INT(10) NOT NULL,
            status ENUM('NEW', 'ASSIGNED', 'PROGRESS_IN', 'COMPLETED', 'FAILED', 'CANCELLED')
            level_risk INT difficulty*2 + importance,
            assigned_agent_id INT DEFAULT NULL
            )""")
        cursor.commit()
        cursor.close()
        conn.close()


