FROM python:3.9 as setup-stage

WORKDIR /tmp/

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --dev
RUN poetry export -f requirements.txt --output requirements-dev.txt --without-hashes


FROM python:3.9 as prod

WORKDIR /app

COPY --from=setup-stage /tmp/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./isitgoingtohell isitgoingtohell/


FROM python:3.9 as dev

WORKDIR /app

COPY --from=setup-stage /tmp/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
