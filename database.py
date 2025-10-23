from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup db url, make engine as connection to the database
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/music_app_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a session to the database, yield the db and close the session after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
