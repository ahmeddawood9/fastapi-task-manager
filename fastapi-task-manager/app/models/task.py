from sqlalchemy import Column, Integer, String, Boolean
# Syntax: Import Base from your core database file
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    # Syntax: Defining the columns for the Postgres table
    # Logic: This tells the warehouse exactly how to store a Task.
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)
