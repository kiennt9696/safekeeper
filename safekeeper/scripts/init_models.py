from sqlalchemy import create_engine

from safekeeper.models import Base

if __name__ == "__main__":
    db_uri = "postgresql+psycopg2://postgres:postgres@127.0.0.1:8432/access?application_name=safekeeper"
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
