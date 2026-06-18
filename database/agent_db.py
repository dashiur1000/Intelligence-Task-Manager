from fastapi import HTTPException
import mysql
class AgentDB:

    def __init__(self, DB_connection):
        self.conn = DB_connection()

    def create_agent(self, data):
        if data == {}:
            raise HTTPException(status_code=422)
        if data["agent_rank"] not in ['Junior', 'Senior', 'Commander']:
            raise HTTPException(status_code=400)
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor()
            sql = "INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)"
            val = (data["name"], data["specialty"], data["agent_rank"])
            cursor.execute(sql, val)
            conn.commit()
            conn.close()
            cursor.close()
            return "Agent Created"
        except:
            raise HTTPException(status_code=422)



    def get_all_agents_all(self):
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents")
            result = cursor.fetchall()
            list_of_agents = []
            for agent in result:
                list_of_agents.append({"id": agent["id"], "name": agent["name"], "specialty": agent["specialty"], "is_active": agent["is_active"], "completed_missions": agent["completed_missions"], "failed_missions": agent["failed_missions"], "agent_rank": agent["agent_rank"]})
            return list_of_agents
        except:
            return []


    def get_agent_by_id(self, id: int):
        conn = self.conn.get_connections()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM agents WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return {"id": result["id"], "name": result["name"], "specialty": result["specialty"], "is_active": result["is_active"], "completed_missions": result["completed_missions"], "failed_missions": result["failed_missions"], "agent_rank": result["agent_rank"]}
        except:
            raise HTTPException(status_code=404)
        finally:
            cursor.close()
            conn.close()


    def update_agent(self, id, data):
        conn = self.conn.get_connections()
        cursor = conn.cursor()
        try:
            set_parts = [f"{key} = %s" for key in data.keys()]
            set_cluse = ", ".join(set_parts)
            sql = f"UPDATE agents SET {set_cluse} WHERE id = %s"
            val = list(data.values()) + [id]
            cursor.execute(sql, val)
            conn.commit()
            return "The operation was successful"
        except:
            raise HTTPException(status_code=404, detail="The operation was unsuccessful")
        finally:
            cursor.close()
            conn.close()



    def deactivate_agent(self, id):
        conn = self.conn.get_connections()
        cursor = conn.cursor()
        try:
            sql = "UPDATE agents SET is_active = 0 WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            return "The operation was successful"
        except:
            return "The operation was unsuccessful"
        finally:
            cursor.close()
            conn.close()

    def increment_completed(self, id):
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT COUNT(status) FROM missions WHERE status = 'COMPLETED' AND assigned_agent_id = %s"
            completed = cursor.execute(sql, id)
            sql = "UPDATE agents SET completed_missions %s WHERE id = %s"
            val = (completed, id)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return "The operation was successful"
        except:
            return "The operation was unsuccessful"


    def increment_failed(self, id):
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT COUNT(status) FROM missions WHERE status = 'FAILED' AND assigned_agent_id = %s"
            failed = cursor.execute(sql, id)
            sql = "UPDATE agents SET completed_missions %s WHERE id = %s"
            val = (failed, id)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return "The operation was successful"
        except:
            return "The operation was unsuccessful"

    def get_agent_performance(self, id):
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT COUNT(status) FROM missions WHERE status = 'COMPLETED' AND assigned_agent_id = %s"
            cursor.execute(sql, id)
            completed = cursor.fetchone()
            sql = "SELECT COUNT(status) FROM missions WHERE status = 'FAILED' AND assigned_agent_id = %s"
            failed = cursor.execute(sql, id)
            total = completed + failed
            success_rate = (completed/total) * 100
            cursor.close()
            conn.close()
            return {"completed": completed, "failed": failed, "total": total, "success_rate": success_rate}
        except:
            return "The operation was unsuccessful"

    def count_active_agent(self):
        conn = self.conn.get_connections()
        cursor = conn.cursor(dictionary=True)
        active = cursor.execute("SELECT COUNT(*) AS counter FROM agents WHERE is_active = TRUE")
        cursor.fetchall()
        return active["count"]


