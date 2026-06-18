from fastapi import APIRouter
from database.agent_db import AgentDB

agent_db = AgentDB(DB_connection)
router = APIRouter()

@router.post("agents")
def create_new_agent(data: dict):
    return agent_db.create_agent(data)