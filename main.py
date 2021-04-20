from base import engine, Base
from models import Patient, Procedure, Encounter, Procedure


def main():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
