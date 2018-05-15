# TSWIFT project

Tswift is an app to management task in Kanbans board
one of the main features is the user can share
boards with groups and users to work as team or just
to plan any activity

## About project

This repository it will control backend app
with api rest.

You can access documentation on `/api/docs`

## Requirements

* Python 3.6.2
* Docker 17 or +
* Docker-compose 3
* Postgres
* Ubuntu 17.10 (Development enviroment actually)
* Nginx

## Deploy with docker

1. Create a `.env` file with the next structure:
    ```
    DJANGO_SETTINGS_MODULE=project.settings_prod # Try dont change this
    ALLOWED_HOSTS=0.0.0.0 # Try dont change this
    APP_SECRET=Some_secret_goes_here:)
    POSTGRES_DB=database_name
    POSTGRES_HOST=postgres # Try dont change this
    POSTGRES_PORT=database_port
    POSTGRES_USER=database_user
    POSTGRES_PASSWORD=database_pass
    REDIS_CACHE_LOCATION=ip_port_location_redis
    DEFAULT_FROM_EMAIL=from email
    EMAIL_HOST=email host
    EMAIL_PORT=email port
    EMAIL_HOST_USER=username host email
    EMAIL_HOST_PASSWORD=password host email
    ```
2. Execute `docker-compose up -d`
3. Goes to your `<allowed_host>:8000` direction to check works properly
4. execute `ln -s /path/to/app/nginx.conf /etc/nginx/sites-enabled/tswif`
5. restart nginx server with `sudo systemctl restart nginx`
6. enjoy your app :)

Note: Delete `# Try dont change this` because it will fail at import
environment variable

# Info docker-compose services
Docker compose contains 3 services to up tswift-backend:

1. django: Backend (API)
2. postgres: Data base (Data storage)
3. redis: Cache (Cache storage)

# Authentication

Authentication backend it's gonna be with json web tokens over the URI
`/api/v1/login/`. If the user fails 3 times the backend will be block
his ip and user-agent 1 minute.

## Authors

Main: Ángel Berhó Grande (Bergran)