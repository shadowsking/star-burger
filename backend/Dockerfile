FROM python:3.11-alpine

WORKDIR /opt/app

COPY backend .
COPY .env .
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python manage.py collectstatic --noinput && \
    gunicorn -w 5 -b 0.0.0.0:8000 star_burger.wsgi:application"]
