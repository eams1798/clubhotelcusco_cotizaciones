FROM python:3.8.13

WORKDIR /home/app/clubhotelcusco_cotizaciones

ENV FLASK_APP api/v1/app.py

ENV FLASK_RUN_HOST 0.0.0.0

# RUN apk add --no-cache gcc musl-dev linux-headers

RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get install -y python3-lxml zlib1g-dev
RUN pip install Flask flask_cors mysqlclient SQLAlchemy

COPY . .

CMD ["python", "-m", "api.v1.app"]
