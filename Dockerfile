FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=weather_api.settings
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "weather_api.wsgi:application"]
