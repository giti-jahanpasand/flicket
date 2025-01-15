# Base Image
FROM docker.arvancloud.ir/python:3.12

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependencies files
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the application port
EXPOSE 5000
WORKDIR /app/src
# Entry point to run the necessary commands before starting the app
ENTRYPOINT ["sh", "-c", "python create_db_config.py && flask db upgrade && flask run-set-up && gunicorn --bind 0.0.0.0:5000 application:app"]
