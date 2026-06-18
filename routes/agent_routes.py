from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.db_connection import DB_connection

router = APIRouter()
agent_db = AgentDB(DB_connection)


@router.post("/agents", status_code=201)
def create_new_agent(data: dict):
    return agent_db.create_agent(data)

@router.get("/agents")
def get_all_agents_all():
    return agent_db.get_all_agents_all()

@router.get("/agents/{id}")
def get_agent_by_id(id):
    try:
        id = int(id)
        return agent_db.get_agent_by_id(id)
    except:
        if id == int(id):
            raise HTTPException(status_code=404)
