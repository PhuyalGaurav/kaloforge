FROM python:3.12 AS builder

ARG SECRET_KEY
ARG DEBUG
ARG DATABASE_URL
ARG API_KEY
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV DATABASE_URL=${DATABASE_URL}
ENV API_KEY=${API_KEY}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/static/resume /app/staticfiles \
    && chmod -R 755 /app/static /app/staticfiles
RUN python manage.py collectstatic --noinput

CMD exec gunicorn config.wsgi:application --config gunicorn.conf.py