from fastapi import APIRouter, HTTPException
from database.mission_db import MissionDB
from database.db_connection import DB_connection

router = APIRouter()
mission_db = MissionDB(DB_connection)


@router.post("/missions")
def create_missions(data: dict):
    return mission_db.create_mission(data)

@router.get("/missions")
def get_all_mission():
    return mission_db.get_all_missions()

@router.get("/missions/{id}")
def get_mission_by_id(id: int):
    return mission_db.get_mission_by_id(id)