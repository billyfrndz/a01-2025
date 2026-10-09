FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py init_db.py ./
COPY templates/ ./templates/

# Initialize DB at build time (or run manually)
RUN mkdir -p /app/data && python init_db.py

EXPOSE 5000
CMD ["python", "app.py"]