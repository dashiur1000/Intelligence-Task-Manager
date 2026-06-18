from fastapi import APIRouter, HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from database.db_connection import DB_connection, logger

router = APIRouter()
mission_db2 = MissionDB(DB_connection)
agent_db2 = AgentDB(DB_connection)


@router.get("/reports/summary")
def get_summary():
    return {"active_agents_count": agent_db2.count_active_agent(),
            "total_missions": mission_db2.count_all_missions(),
            "open_missions": mission_db2.count_open_missions}


@router.get("/reports/top-agent")
def get_top():
    return agent_db2.get_top()