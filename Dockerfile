FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install nc (optional, can be removed if unused now)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Collect static files at build time
RUN python manage.py collectstatic --noinput

# Expose the port Django runs on
EXPOSE 8000

# Run the application using gunicorn
CMD ["gunicorn", "ticket_booking.wsgi:application", "--bind", "0.0.0.0:8000"]
