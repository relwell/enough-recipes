FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y default-libmysqlclient-dev nodejs npm

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml /usr/src/app/

RUN pip install poetry

RUN poetry install --no-dev

ADD . .

# could use multi-stage here for a slimmer image.
# consumer and producer don't need this.
# neither would any API.
RUN poetry run python manage.py tailwind build
