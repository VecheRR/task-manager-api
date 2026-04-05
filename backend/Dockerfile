FROM python:3.11

WORKDIR /app

COPY . .

# Потом разобраться с uv
# RUN pip install uv
# RUN uv pip install -r pyproject.toml

RUN pip install fastapi uvicorn psycopg2-binary sqlalchemy

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]