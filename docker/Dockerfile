FROM python:3.13-slim
WORKDIR /app
COPY max_portfolio/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY max_portfolio /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]