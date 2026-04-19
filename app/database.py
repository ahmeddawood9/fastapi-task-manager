from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Syntax: Connection string for your actual Task Manager database

# Syntax: postgresql://username:password@host:port/database_name
# Logic: We are switching back to the 'dawood_dev' user and 'learning_db' warehouse you already created in psql.
SQLALCHEMY_DATABASE_URL = "postgresql://dawood_dev:learning123@localhost:5432/learning_db"

# Syntax: Create the Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Syntax: Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Syntax: The Base class for all models
Base = declarative_base()

# Syntax: Dependency Generator
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
