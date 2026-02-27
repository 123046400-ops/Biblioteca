FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn email-validator

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]