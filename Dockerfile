FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD python3 -m flask db upgrade && python3 -m gunicorn -w 4 --preload -b 0.0.0.0:5000 app:app