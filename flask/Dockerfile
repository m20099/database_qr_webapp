FROM python:3.11-bullseye

RUN pip install Flask Flask-SQLAlchemy flask-cors mysqlclient

WORKDIR /app
COPY . .

EXPOSE 5000

CMD ["python", "index.py"]
