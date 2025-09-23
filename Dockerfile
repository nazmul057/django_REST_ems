FROM python:3.12.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /ems_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /ems_app/django_entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/ems_app/django_entrypoint.sh"]
