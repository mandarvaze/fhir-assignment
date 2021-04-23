# Requirements

- Docker
- Python 3.8

# Setup

```shell
python -m venv .venv-prometheus
source .venv-prometheus/bin/activate
pip install -r requirements.txt
pre-commit install  # Only for development
```

# Start postgres

- `make start-pgsql` (To start in the background)
- `make pgsql` (To start in the foreground - sometimes this is helpful to troubleshoot)
- Use `docker ps` to ensure that postgres has actually started

# Get the code and data files

``` shell
$ git clone git@github.com:mandarvaze/fhir-assignment.git
$ cd fhir-assignment
$ mkdir data
```

# Download the data files

Download these files in the `data` folder we created in the previous step

1. https://github.com/smart-on-fhir/flat-fhir-files/blob/master/r3/Patient.ndjson
2. https://github.com/smart-on-fhir/flat-fhir-files/blob/master/r3/Observation.ndjson
3. https://github.com/smart-on-fhir/flat-fhir-files/blob/master/r3/Encounter.ndjson
4. https://github.com/smart-on-fhir/flat-fhir-files/blob/master/r3/Procedure.ndjson

# Usage

1. First import the data into the database

`$ python main.py -i`

This step can take really long time, but it shows progress via "one dot per record" - so you won't think it had hung.
I will optimize this part later.

2. Now you can generate the report

`$ python main.py -r`
