from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.db_connection import DB_connection, logger

router = APIRouter()
agent_db = AgentDB(DB_connection)


@router.post("/agents", status_code=201)
def create_new_agent(data: dict):
    logger.info("post /agents")
    try:
        logger.info("create new agent")
        return agent_db.create_agent(data)
    except KeyError:
        logger.error("Invalid rank entered")
        raise HTTPException(status_code=400)

@router.get("/agents")
def get_all_agents_all():
    logger.info("get /agents")
    return agent_db.get_all_agents_all()

@router.get("/agents/{id}")
def get_agent_by_id(id):
    logger.info("get /agents/{id}")
    try:
        id = int(id)
        return agent_db.get_agent_by_id(id)
    except:
        logger.error("Something is wrong")
        try:
            if id == int(id):
                logger.error("No such agent exists")
                raise HTTPException(status_code=404)
        except ValueError:
            logger.error("No number entered at all")
            raise HTTPException(status_code=422)

@router.put("/agents/{id}")
def update_agent(id, data: dict):
    logger.info("put /agents/{id}")
    try:
        id = int(id)
        logger.info("update agent")
        return agent_db.update_agent(id, data)
    except:
        logger.error("There is an error in the data")
        try:
            if data == {} and id == int(id):
                logger.error("The dictionary is empty")
                raise HTTPException(status_code=422)
            elif id == int(id):
                logger.error("The agent was not found")
                raise HTTPException(status_code=404)
        except ValueError:
            logger.error("An invalid character was entered")
            raise HTTPException(status_code=422)


@router.put("/agents/{id}/deactivate")
def deactivate_agent(id):
    logger.info("put /agents/{id}/deactivate")
    try:
        id = int(id)
        logger.info("Update Complete")
        return agent_db.deactivate_agent(id)
    except:
        try:
            if id == int(id):
                logger.error("The agent was not found")
                raise HTTPException(status_code=404)
        except ValueError:
            logger.error("An invalid character was entered")
            raise HTTPException(status_code=422)

@router.get("/agents/{id}/performance")
def get_agent_performance(id):
    logger.info("get /agents/{id}/performance")
    try:
        id = int(id)
        logger.info("Brought the result")
        return agent_db.get_agent_performance(id)
    except:
        try:
            if id == int(id):
                logger.error("The agent was not found")
                raise HTTPException(status_code=404)
        except ValueError:
            logger.error("An invalid character was entered")
            raise HTTPException(status_code=422)

