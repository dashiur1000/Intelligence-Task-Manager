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
