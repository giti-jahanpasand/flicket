#! /bin/sh
usermod -d /var/lib/mysql mysql

service mariadb start 2>/dev/null

if [ -f /docker-entrypoint-initdb.d/init.sql ]; then
    envsubst < /docker-entrypoint-initdb.d/init.sql | mysql -u root
    echo "Databases initialized successfully."
else
    echo "init.sql not found. Skipping database initialization."
fi

python3 create_db_config.py
flask db upgrade
flask run-set-up
exec gunicorn --bind 0.0.0.0:5000 application:app

