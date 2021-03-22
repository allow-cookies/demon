# DEMON

**DEMON** is a **DE**pendency **MON**itoring tool. It allows you to list and monitor all
the dependencies used across all of your projects. 

## Setup

> **Prerequisites:** Docker, docker-compose

1. Clone this repository.
1. Create `.env` file basing on the existing `.env.example` file.
1. Run `docker-compose up -d` and wait for all containers to be up and running.
1. Run migrations: `docker-compose exec django python manage.py migrate`
1. Visit http://localhost:8000 in your favourite browser.