FROM python:3.12 AS builder

ARG SECRET_KEY
ARG DEBUG

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]