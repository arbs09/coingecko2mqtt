FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV BROKER=""
ENV BROKER_PORT=""
ENV BROKER_USERNAME=""
ENV BROKER_PASSWORD=""
ENV SLEEP_TIME=""
ENV COINGECKO_KEY=""
ENV CORRENCY=""
ENV COIN = ""

CMD ["python", "app.py"]