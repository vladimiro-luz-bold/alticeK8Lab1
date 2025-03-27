# Use a base Python image
FROM python:3.9-slim

# Install necessary system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies using pip
RUN pip install --no-cache-dir flask flask-bcrypt psycopg2

# Copy the application files to the container
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]