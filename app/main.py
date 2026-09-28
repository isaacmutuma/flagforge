"""
FastAPI app entry point. Creates tables on startup (fine for this
stage — a real migration tool like Alembic replaces this once the
schema needs to evolve without dropping data) and wires in the
routers.
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import flags

Base.metadata.create_all(bind=engine)

app = FastAPI(title="flagforge", description="A feature flag service.")

app.include_router(flags.router)


@app.get("/")
def root():
    return {"status": "flagforge is running"}