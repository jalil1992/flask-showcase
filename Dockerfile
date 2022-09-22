FROM python:3.8-slim

ARG SSH_PRIVATE_KEY
ARG PYPI_USERNAME
ARG PYPI_PASSWORD

RUN apt-get update && apt-get install -y git ssh gcc g++ libpq-dev \
    libxml2-dev libxslt-dev zlib1g-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    postgresql-client --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN echo "machine pypi.service_name.com\n    login ${PYPI_USERNAME}\n    password ${PYPI_PASSWORD}" > /root/.netrc
RUN chown root ~/.netrc
RUN chmod 0600 ~/.netrc

RUN mkdir /root/.ssh/ && \
    echo "${SSH_PRIVATE_KEY}"|base64 -d > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 700 /root/.ssh && \
    touch /root/.ssh/known_hosts && \
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

RUN mkdir -p /app
WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn_settings.py", "api.wsgi:app"]