class MissionDB:
    def __init__(self, DB_connection):
        self.conn = DB_connection

    def create_mission(self, data):
        conn = self.conn
        cursor = conn.cursor()
        sql = "INSERT INTO missions (title, description, location, difficulty, importance, status, level_risk) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (data["title"], data["description"], data["location"], data["difficulty"], data["importance"], self.definition_risk_level(data["difficulty"], data["importance"]))
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        cursor.close()
        num_id = cursor.lastrowid
        return self.get_mission_by_id(num_id)

    def get_all_missions(self):
        try:
            conn = self.conn
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions")
            result = cursor.fetchall()
            list_of_missions = []
            for mission in result:
                list_of_missions.append({"id": mission["id"],
                                         "title": mission["title"],
                                         "description": mission["description"],
                                         "location": mission["location"],
                                         "difficulty": mission["difficulty"],
                                         "importance": mission["importance"],
                                         "status": mission["status"],
                                         "risk_level": mission["risk_level"],
                                         "assigned_agent_id": mission["assigned_agent_id"]})
            return list_of_missions
        except:
            return []

    def get_mission_by_id(self, id):
        try:
            conn = self.conn
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM missions WHERE id = %s"
            cursor.execute(sql, id)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return {"id": result["id"],
                    "title": result["title"],
                    "description": result["description"],
                    "location": result["location"],
                    "difficulty": result["difficulty"],
                    "importance": result["importance"],
                    "status": result["status"],
                    "risk_level": result["risk_level"],
                    "assigned_agent_id": result["assigned_agent_id"]}
        except:
            return None

    def assign_mission(self, m_id, a_id):
        try:
            conn = self.conn
            cursor = conn.cursor(dictionary=True)
            check = self.checker_to_associate_with_agent(a_id)
            if check == True:
                sql = "UPDATE missions SET assigned_agent_id = %s WHERE id = %s"
                val = (a_id, m_id)
                cursor.execute(sql, val)
                conn.commit()
                cursor.close()
                conn.close()
                return "The operation was successful"
        except:
            return "The operation was unsuccessful"

    def update_mission_status(self, status):
        pass

    def get_open_missions_by_agent(self, id):
        pass

    def count_all_missions(self):
        pass

    def count_by_status(self, status):
        pass

    def count_open_missions(self):
        pass

    def count_critical_missions(self):
        pass

    def get_top_agent(self):
        pass

    def definition_risk_level(self, difficulty: int, importance: int):
        result = difficulty * 2 + importance
        risk_level = ""
        if result <= 9:
            risk_level = "LOW"
        elif result <= 17:
            risk_level = "MEDIUM"
        elif result <= 24:
            risk_level = "HIGH"
        elif result > 24:
            risk_level = "CRITICAL"
        return risk_level

    def checker_to_associate_with_agent(self, id):
        conn = self.conn
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT COUNT(assigned_agent_id) FROM agents WHERE 'assigned_agent_id' = %s AND 'status' = %s OR 'status' = %s"
        val = (id, "ASSIGNED", "IN_PROGRESS")
        sum_missions_to_agent = cursor.execute(sql, val)
        if sum_missions_to_agent < 3:
            sql = "SELECT is_active FROM agents WHERE id = %s"
            val = (id,)
            active = cursor.execute(sql, val)
            if active.fetchall() == "TRUE":
                return True
            return False
        return False

