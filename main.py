from fastapi import FastAPI
import uvicorn
from database.db_connection import DB_connection
from routes.mission_routes import router as mission_db
from routes.report_routes import router as report_routes
from routes.agent_routes import router as agent_routes
app = FastAPI()
app.include_router(agent_routes)
app.include_router(mission_db)
app.include_router(mission_db)
app.include_router(report_routes)


my_conn = DB_connection()

def main():
    my_conn.create_database()
    my_conn.create_tables()
    uvicorn.run("main:app", port=8008)

if __name__ == "__main__":
    main()