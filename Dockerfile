# Base Image
FROM python:3.13

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
COPY src/ /app/

# Expose the application port
EXPOSE 5000

ENTRYPOINT ["bash", "-c", "./entrypoint.sh"]