
# Start database in docker in foreground
.PHONY: pgsql
pgsql:
	@docker stop pr-fhir-pgsql || true
	@docker rm pr-fhir-pgsql || true
	@docker run -it --rm --name pr-fhir-pgsql -v $(shell pwd)/.docker:/docker-entrypoint-initdb.d -e POSTGRES_PASSWORD=5ecr3TPa55 -p 5432:5432 postgres:12-alpine \
		postgres -c 'log_statement=all' -c 'max_connections=1000' -c 'log_connections=true'  -c 'log_disconnections=true'  -c 'log_duration=true'

# Start database in docker in background
.PHONY: start-pgsql
start-pgsql:
	docker start pr-fhir-pgsql || docker run -d -v $(shell pwd)/.docker:/docker-entrypoint-initdb.d -e POSTGRES_PASSWORD=5ecr3TPa55 -p 5432:5432 --name pr-fhir-pgsql postgres:12-alpine

.PHONY: clean-pgsql
clean-pgsql:
	@docker stop pr-fhir-pgsql || true
	@docker rm pr-fhir-pgsql || true

.PHONY: stop-pgsql
stop-pgsql:
	@docker stop pr-fhir-pgsql || true

# Testing and linting targets
.PHONY: lint
lint:
	@pre-commit run --all-files

# anything, in regex-speak
filter = "."

# additional arguments for pytest
unit_test_all = "false"
ifeq ($(filter),".")
	unit_test_all = "true"
endif
ifdef path
	unit_test_all = "false"
endif
pytest_args = tests -v -k $(filter)
coverage_args = ""
ifeq ($(unit_test_all),"true")
	coverage_args = --cov=. --cov-branch --cov-report term-missing
endif

.PHONY: unit
unit:
ifndef path
	@pytest $(coverage_args) $(pytest_args)
else
	@pytest
endif

.PHONY: tests
# tests: format lint types unit
tests: lint unit
