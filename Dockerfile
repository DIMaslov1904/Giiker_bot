FROM python:3.12-slim
LABEL authors="DIMaslov"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app .

ENTRYPOINT ["python", "bot.py"]
