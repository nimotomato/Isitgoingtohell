FROM python:3.9-slim-buster as setup-stage

# python
# sends log directly to stdout streams wihtout being buffered
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # poetry
    POETRY_VERSION=1.1.12 \
    POETRY_NO_INTERACTION=1 


WORKDIR /app

RUN pip install poetry 

# as we are already inside a docker env we dont need
# to create a new venv inside the docker
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

# install env
RUN poetry install --no-dev

# # run p
# ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

COPY ./isitgoingtohell isitgoingtohell/

CMD ["python", "-m", "isitgoingtohell.main"]