from fastapi import HTTPException
import mysql
from database.db_connection import logger

class AgentDB:

    def __init__(self, DB_connection):
        self.conn = DB_connection()

    def create_agent(self, data):
        if data == {}:
            logger.error("Empty dictionary")
            raise HTTPException(status_code=422)
        if data["agent_rank"] not in ['Junior', 'Senior', 'Commander']:
            logger.error("Invalid rank entered.")
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
            logger.info("The addition operation was successful.")
            return "Agent Created"
        except:
            logger.error("The insert operation is incorrect.")
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
            logger.info("Showing all agents")
            return list_of_agents
        except:
            logger.error("No agents")
            return []


    def get_agent_by_id(self, id: int):
        conn = self.conn.get_connections()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM agents WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            logger.info("Introducing the agent")
            return {"id": result["id"], "name": result["name"], "specialty": result["specialty"], "is_active": result["is_active"], "completed_missions": result["completed_missions"], "failed_missions": result["failed_missions"], "agent_rank": result["agent_rank"]}
        except:
            logger.error("Agent does not exist")
            raise HTTPException(status_code=404)
        finally:
            cursor.close()
            logger.info("Closing the connection")
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
            logger.info("Update completed")
            return "The operation was successful"
        except:
            logger.error("The operation was unsuccessful")
            raise HTTPException(status_code=404, detail="The operation was unsuccessful")
        finally:
            cursor.close()
            conn.close()
            logger.info("Closing the connection")




    def deactivate_agent(self, id):
        conn = self.conn.get_connections()
        cursor = conn.cursor()
        try:
            sql = "UPDATE agents SET is_active = 0 WHERE id = %s"
            cursor.execute(sql, (id,))
            changed = cursor.rowcont
            if changed == 0:
                logger.error("No such ID exists")
                raise HTTPException(status_code=404)
            conn.commit()
            logger.info("Updated to deactivate")
            return "The operation was successful"
        except:
            logger.error("Failed to update")
            raise HTTPException(status_code=404, detail="The operation was unsuccessful")
        finally:
            cursor.close()
            conn.close()
            logger.info("Closing the connection")


    def increment_completed(self, id):
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT COUNT(*) as cnt FROM missions WHERE status = 'COMPLETED' AND assigned_agent_id = %s"
            cursor.execute(sql, (id,))
            completed = cursor.fetchone()['cnt']
            sql = "UPDATE agents SET completed_missions = %s WHERE id = %s"
            val = (completed, id)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("Closing the connection")
            logger.info("The operation was successful")
            return "The operation was successful"
        except:
            logger.error("Failed to update")
            raise HTTPException(status_code=422)


    def increment_failed(self, id):
        try:
            conn = self.conn.get_connections()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT COUNT(*) as cnt FROM missions WHERE status = 'FAILED' AND assigned_agent_id = %s"
            cursor.execute(sql, (id,))
            failed = cursor.fetchone()['cnt']
            sql = "UPDATE agents SET completed_missions %s WHERE id = %s"
            val = (failed, id)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("The operation was successful")
            return "The operation was successful"
        except:
            logger.error("Failed to update")
            raise HTTPException(status_code=422)

    def get_agent_performance(self, id):
        conn = self.conn.get_connections()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT COUNT(*) as cnt FROM missions WHERE status = 'COMPLETED' AND assigned_agent_id = %s"
            cursor.execute(sql, (id,))
            completed = cursor.fetchone()['cnt']
            sql = "SELECT COUNT(*) as cnt FROM missions WHERE status = 'FAILED' AND assigned_agent_id = %s"
            cursor.execute(sql, (id,))
            failed = cursor.fetchone()['cnt']
            total = completed + failed
            if total > 0:
                success_rate = (completed/total) * 100
                logger.info("Showing final result")
                return {"completed": completed, "failed": failed, "total": total, "success_rate": success_rate}
            else:
                logger.error("Cannot divide by 0")
                raise ZeroDivisionError("ZeroDivisionError")
        except:
            logger.error("No such agent found")
            raise HTTPException(status_code=404)
        finally:
            cursor.close()
            conn.close()
            logger.info("Closing the connection")


    def count_active_agent(self):
        logger.info("Counts active agents")
        conn = self.conn.get_connections()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS counter FROM agents WHERE is_active = TRUE")
        active = cursor.fetchone()
        logger.info("Keeps track of active soldiers")
        return active["count"]

    def get_top(self):
        logger.info("Checks who is most active")
        conn = self.conn.get_connections()
        cursor = conn.cursor()
        cursor.execute("SELECT completed_missions FROM agents GROUP BY DESC")
        completed = cursor.fetchone()
        logger.info("Returns the most active")
        return completed


