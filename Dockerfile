FROM python:3.11.1-alpine3.17

ENV POETRY_VERSION=1.3.2

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY . .

RUN poetry install --no-dev --no-interaction --no-ansi

CMD [ "poetry", "run", "bot" ]