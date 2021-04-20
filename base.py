from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://dev:dev@localhost:5432/pr-fhir')
Session = sessionmaker(bind=engine)

Base = declarative_base()
