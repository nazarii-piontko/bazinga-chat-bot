FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /app
RUN chmod +x wait-for-it.sh

COPY main.py /app

CMD python main.py
