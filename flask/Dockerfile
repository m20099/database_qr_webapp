FROM python:3.11-bullseye

RUN pip install Flask Flask-SQLAlchemy flask-cors mysqlclient flask_jwt_extended datetime flask_bcrypt python-dotenv

WORKDIR /app
COPY . .

EXPOSE 5000

CMD ["python", "index.py"]
