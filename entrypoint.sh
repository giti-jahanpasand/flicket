#! /bin/bash
python create_db_config.py
flask db upgrade
gunicorn --bind 0.0.0.0:5000 application:app
