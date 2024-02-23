FROM python:3.11

WORKDIR /code

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry config virtualenvs.create false && poetry install

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
