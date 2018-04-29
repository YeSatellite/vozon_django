sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

pip install psycopg2-binary

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

postgres=# 
CREATE DATABASE car_db;
CREATE USER car_user WITH PASSWORD 'password';
ALTER ROLE car_user SET client_encoding TO 'utf8';
ALTER ROLE car_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE car_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE car_db TO car_user;
postgres=# 


sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv


sudo ln -f tools/gunicorn.service /etc/systemd/system/

sudo ln -f tools/car.nginx /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/car.nginx /etc/nginx/sites-enabled

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

sudo nginx -t && sudo systemctl restart nginx