# Base Image
FROM docker.arvancloud.ir/ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
apt-get install -y python3 python3-pip mariadb-server gettext-base && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/init.sql /docker-entrypoint-initdb.d/
COPY . .

# Expose the application port
EXPOSE 5000
WORKDIR /app/src

COPY entrypoint.sh /app/src
RUN chmod +x /app/src/entrypoint.sh
# Entry point to run the necessary commands before starting the app
ENTRYPOINT ["/app/src/entrypoint.sh"]