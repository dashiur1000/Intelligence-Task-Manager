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
        try:
            if id == int(id):
                raise HTTPException(status_code=404)
        except ValueError:
            raise HTTPException(status_code=422)

@router.put("/agents/{id}")
def update_agent(id, data: dict):
    try:
        id = int(id)
        return agent_db.update_agent(id, data)
    except:
        try:
            if data == {} and id == int(id):
                raise HTTPException(status_code=422)
            elif id == int(id):
                raise HTTPException(status_code=404)
        except ValueError:
            raise HTTPException(status_code=422)


@router.put("/agents/{id}/deactivate")
def deactivate_agent(id):
    try:
        id = int(id)
        return agent_db.deactivate_agent(id)
    except:
        try:
            if id == int(id):
                raise HTTPException(status_code=404)
        except ValueError:
            raise HTTPException(status_code=422)

@router.get("/agents/{id}/performance")
def get_agent_performance(id):
    try:
        id = int(id)
        return agent_db.get_agent_performance(id)
    except:
        try:
            if id == int(id):
                raise HTTPException(status_code=404)
        except ValueError:
            raise HTTPException(status_code=422)

