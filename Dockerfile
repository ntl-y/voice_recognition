FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

COPY . .

EXPOSE 7777

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7777"]
