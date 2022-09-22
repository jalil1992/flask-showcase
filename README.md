# Flask API Showcase

_This repository is not a working solution. It is abstracted from a flask based microservice that I built before._

A microservice that serves all needs of **_ calculation.
This is just a wrapper of _** library and `flask` was used to serve requests. (`flask-morest`)

## Status

| Date       | \*\*\* Version                           |
| ---------- | ---------------------------------------- |
| 2022-05-16 | 92be9ea21ae858056a0e9b5dc17dda5f83cd05f4 |
| 2022-05-19 | 05cd9c690cb5b70df650f8df93dbbb6feb01968c |

## Description

The service is stateless.
It only delegates the calculation to the \*\*\* library and returns the result.

## Dev Environment

For package maintenance, `pip-tools` is used.
The minimum required packages are listed in `requirements.in`.
Whenever a command `pip-compile --upgrade` is executed, `requirements.txt` is generated/updated automatically.

```
# virtual env activated
pip install pip-tools
pip-compile --upgrade
pip install -r requirements.txt
make start
```

You can simply run `make` in the root of the folder to see the available commands.

## Running tests

`make test` runs the tests

On every push to `develop` branch, tests will be executed.

## Build

`make build` builds a docker image.

On every push to `master` branch, a new version of docker image is built and pushed to hub.

## Deployment

On every push to `deploy` branch, the corresponding pipeline `deploy-***-analysis-service` on [helmchart](https://bitbucket.org/***/helm-charts/src/main/bitbucket-pipelines.yml) repo will be triggered.
This updates the pod running on the cluster at `http://***-analysis-internal.***.us`.

## API Documentation

`make openapi-push` creates `openapi.json` from the code and pushes to Swagger Hub at https://app.swaggerhub.com/apis/***/***-analysis/.
