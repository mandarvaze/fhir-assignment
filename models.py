from sqlalchemy import (
    Column,
    Text,
    Integer,
    Date,
    ForeignKey,
    DateTime,
    DECIMAL)

from base import Base


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Text, nullable=False)
    birth_date = Column(Date)
    gender = Column(Text)
    race_code = Column(Text)
    race_code_system = Column(Text)
    ethnicity_code = Column(Text)
    ethnicity_code_system = Column(Text)
    country = Column(Text)


class Encounter(Base):
    __tablename__ = 'encounter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Text, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    type_code = Column(Text)
    type_code_system = Column(Text)


class Procedure(Base):
    __tablename__ = 'procedure'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Text, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    encounter_id = Column(Integer, ForeignKey('encounter.id'))
    procedure_date = Column(Date, nullable=False)
    type_code = Column(Text, nullable=False)
    type_code_system = Column(Text, nullable=False)


class Observation(Base):
    __tablename__ = 'observation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Text, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    encounter_id = Column(Integer, ForeignKey('encounter.id'))
    observation_date = Column(Date, nullable=False)
    type_code = Column(Text, nullable=False)
    type_code_system = Column(Text, nullable=False)
    value = Column(DECIMAL)
    unit_code = Column(Text)
    unit_code_system = Column(Text)
