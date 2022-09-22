##########################################################################
# This is the project's makefile.
#
# You can build, test, setup fixtures, start, stop,
# export, run commands, etc.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################
TAG := ***-analysis
PORT := 5050

###############################################################################
# HELP / DEFAULT COMMAND
###############################################################################
.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##########################################################################
# BUILD
##########################################################################

.PHONY: build
build: ## Build the ***-api service as a docker image
	docker build --build-arg SSH_PRIVATE_KEY="$(shell cat ~/.ssh/id_rsa|base64 -b0)" -t $(TAG) --build-arg PYPI_USERNAME=$(shell echo $(PYPI_USERNAME)) --build-arg PYPI_PASSWORD=$(shell echo $(PYPI_PASSWORD)) .

##########################################################################
# START & STOP
##########################################################################

.PHONY: start
start: ## start ***-api service (local dev)
	. venv/bin/activate && FLASK_APP=./api/app.py FLASK_ENV=development python -m flask run --port=5050

.PHONY: start-gunicorn
start-gunicorn: ## start ***-api service with gunicorn
	. venv/bin/activate && gunicorn -c gunicorn_settings.py api.wsgi:app

.PHONY: docker-start
docker-start:  ## start ***-api docker container
	# make build
	docker container stop $(TAG) || true
	docker container rm $(TAG) || true
	docker run \
		--rm \
		--name $(TAG) \
		-v $$PWD:/app \
		-p $(PORT):$(PORT) \
		-it $(TAG)

.PHONY: docker-stop
docker-stop: ## stop ***-api container
	docker container stop ***-api || true

.PHONY: docker-logs
docker-logs: ##
	docker container logs -f ***-api

##########################################################################
# TEST
##########################################################################
.PHONY: test
test: ## run tests
	. venv/bin/activate && python -m pytest -s --disable-pytest-warnings

.PHONY: clean
clean: ## clean py cache
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

##########################################################################
# OPENAPI
##########################################################################
.PHONY: openapi
openapi: ## save openapi specification as json
	. venv/bin/activate && FLASK_APP=./api/app.py FLASK_ENV=development python -m flask openapi write openapi.json

.PHONY: openapi-push
openapi-push: ## push open api to swaggerhub. api key is supposed to be defined in the environment
	. venv/bin/activate && FLASK_APP=./api/app.py FLASK_ENV=development python -m flask openapi write openapi.json
	curl -X POST "https://api.swaggerhub.com/apis/service_name/***-analysis" \
	-H "Authorization: $(SWAGGER_API_KEY)" \
	-H "Content-Type: application/json" \
	--data-binary @openapi.json