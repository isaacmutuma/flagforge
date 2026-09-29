"""
FastAPI app entry point. Creates tables on startup (fine for this
stage — a real migration tool like Alembic replaces this once the
schema needs to evolve without dropping data) and wires in the
routers.
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import flags

from app.routers import evaluate, flags

'''
creates the database table  in the startup phase
'''
Base.metadata.create_all(bind=engine)
'''
initializes fastAPI
'''
app = FastAPI(title="flagforge", description="A feature flag service.")


#When main.py runs, it registers all routes into one big Routing Table inside the FastAPI instance.
app.include_router(flags.router)
app.include_router(evaluate.router)

@app.get("/")
def root():
    return {"status": "flagforge is running"}