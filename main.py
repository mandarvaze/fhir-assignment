import ndjson
from base import engine, Base
from models import Patient, Procedure, Encounter, Observation  # noqa


def import_data(datafile):
    print(datafile)
    count = 0
    with open(datafile) as f:
        reader = ndjson.reader(f)
        for line in reader:
            print(line.keys())
            count += 1
            break

    print(count)


def main():
    Base.metadata.create_all(engine)
    import_data('./data/Patient.ndjson')
    import_data('./data/Encounter.ndjson')
    import_data('./data/Procedure.ndjson')
    import_data('./data/Observation.ndjson')


if __name__ == '__main__':
    main()
