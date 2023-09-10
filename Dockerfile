FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IN_OPEN_DOCKER 1

RUN apt-get update && apt-get install -y \
    postgresql-client

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:9000"]
