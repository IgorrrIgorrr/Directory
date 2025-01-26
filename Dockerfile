FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN pip install --no-cache-dir poetry==1.8.2

RUN poetry config virtualenvs.create false && \
	poetry install --without dev --no-interaction --no-ansi

COPY . .

EXPOSE 80

CMD ["uvicorn", "directory.main:app", "--host", "0.0.0.0", "--port", "80"]
