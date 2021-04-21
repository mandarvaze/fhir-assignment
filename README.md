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

# Assumptions

The data files are under `data` folder.
