"""
SQLAlchemy ORM models. Week 1 scope: just Flag.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database import Base

'''converting python code to aan actual db table called flags'''
class Flag(Base):
	__tablename__ = "flags"
	id = Column(Integer, primary_key=True, index=True)
	key = Column(String, unique=True, index=True, nullable=False)
	description = Column(String, default="")
	'''
	when a new column is added onto the db it remains hidden and not live the moment it's created
	'''
	enabled = Column(Boolean, default=False, nullable=False)

	'''
	role out of the number of users that see the feature once added
	'''
	rollout_percentage = Column(Integer, default=0, nullable=False)
	'''
	Records when the row was first created
	'''
	created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
	updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

