import ndjson
from base import engine, Base, Session
from models import Patient, Procedure, Encounter, Observation  # noqa
from sqlalchemy.exc import NoResultFound


def ndjson_to_list(datafile):
    with open(datafile) as f:
        reader = ndjson.reader(f)
        data = [line for line in reader]
    return(data)


def import_patients(patients):
    print("Importing Patients")
    count = 0
    session = Session()
    for patient in patients:
        try:
            country = patient['address'][0]['country']
        except KeyError:
            country = 'US'
        patient_obj = Patient(
            source_id=patient['id'],
            birth_date=patient['birthDate'],
            gender=patient['gender'],
            country=country
            # TODO: race, ethnicity
        )
        session.add(patient_obj)
        count += 1
        print(".", end='', flush=True)  # Show progress

    session.commit()
    session.close()
    print(f"\nImported {count} patients")


def import_encounters(encounters):
    print("Importing Encounters")
    count = 0
    session = Session()
    # TODO: Commit intermittently, say after every 100 records
    for encounter in encounters:
        source_id = encounter['subject']['reference'].split('/')[1]
        patient_id = session.query(
            Patient.id).where(
            Patient.source_id == source_id).one().id
        encounter_obj = Encounter(
            source_id=encounter['id'],
            patient_id=patient_id,
            start_date=encounter['period']['start'],
            end_date=encounter['period']['end'],
            type_code=encounter['type'][0]['coding'][0]['code'],
            type_code_system=encounter['type'][0]['coding'][0]['system']
        )
        session.add(encounter_obj)
        count += 1
        print(".", end='', flush=True)  # Show progress

    session.commit()
    session.close()
    print(f"\nImported {count} encounters")


def import_procedures(procedures):
    print("Importing Procedures")
    count = 0
    session = Session()
    for procedure in procedures:
        source_id = procedure['subject']['reference'].split('/')[1]
        patient_id = session.query(
            Patient.id).where(
            Patient.source_id == source_id).one().id
        try:
            procedure_date = procedure['performedDateTime']
        except KeyError:
            procedure_date = procedure['performedPeriod']['start']

        procedure_obj = Procedure(
            source_id=procedure['id'],
            patient_id=patient_id,
            procedure_date=procedure_date,
            type_code=procedure['code']['coding'][0]['code'],
            type_code_system=procedure['code']['coding'][0]['system']
        )
        session.add(procedure_obj)
        count += 1
        print(".", end='', flush=True)  # Show progress

    session.commit()
    session.close()
    print(f"\nImported {count} procedures")


def import_observations(observations):
    print("Importing observations")
    import_count = 0
    record_count = 0
    session = Session()
    # TODO: Commit intermittently, say after every 100 records
    for observation in observations:
        record_count += 1
        source_id = observation['subject']['reference'].split('/')[1]
        try:
            enc_id = observation['context']['reference'].split('/')[1]
        except KeyError as e:
            print(f"{e}: {source_id}")
        try:
            patient_id = session.query(
                Patient.id).where(
                Patient.source_id == source_id).one().id
        except NoResultFound:
            print(f"Patient with source_id {source_id} not found.")
            continue
        try:
            encounter_id = session.query(
                Encounter.id).where(
                Encounter.source_id == enc_id).one().id
        except NoResultFound:
            print(f"Encounter with source_id {enc_id} not found.")
            continue

        try:
            observation_date = observation['effectiveDateTime']
            observation_obj = Observation(
                source_id=observation['id'],
                patient_id=patient_id,
                encounter_id=encounter_id,
                observation_date=observation_date,
                type_code=observation['code']['coding'][0]['code'],
                type_code_system=observation['code']['coding'][0]['system']
            )
        except KeyError as e:
            print(e)
            import pprint
            pprint.pprint(observation)
            continue
        session.add(observation_obj)
        import_count += 1
        print(".", end='', flush=True)  # Show progress

    session.commit()
    session.close()
    print(f"\nImported {import_count} observations out of {record_count}")


def import_data():
    patients = ndjson_to_list('./data/Patient.ndjson')
    import_patients(patients)
    encounters = ndjson_to_list('./data/Encounter.ndjson')
    import_encounters(encounters)
#    procedures = ndjson_to_list('./data/Procedure.ndjson')
#    observations = ndjson_to_list('./data/Observation.ndjson')


def num_records(cls, session):
    from sqlalchemy import func
    rows = session.query(func.count(cls.id)).scalar()
    return rows


def gen_report():
    tables = [Patient, Encounter, Observation, Procedure]
    with Session() as session:
        for table in tables:
            count = num_records(table, session)
            table_name = table.__tablename__.title()
            print(f'Number of {table_name}s : {count}')


def main():
    # We do not want same data imported again if this program
    # is run multiple times so drop all the data first
    # There may be other option like make `source_id` unique,
    # but that is not mentioned in the requirements, hence this approach
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    import_data()
    gen_report()


if __name__ == '__main__':
    main()
