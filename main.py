import ndjson
from base import engine, Base, Session
from models import Patient, Procedure, Encounter, Observation  # noqa


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


def import_data():
    patients = ndjson_to_list('./data/Patient.ndjson')
    import_patients(patients)
    encounters = ndjson_to_list('./data/Encounter.ndjson')
    import_encounters(encounters)
#    procedures = ndjson_to_list('./data/Procedure.ndjson')
#    observations = ndjson_to_list('./data/Observation.ndjson')


def main():
    # We do not want same data imported again if this program
    # is run multiple times so drop all the data first
    # There may be other option like make `source_id` unique,
    # but that is not mentioned in the requirements, hence this approach
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    import_data()


if __name__ == '__main__':
    main()
