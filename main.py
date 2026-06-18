from fastapi import FastAPI

from routes.agent_routes import router as agent_routes

def main():
    agent_routes()