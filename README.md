![DeMon_logo](https://user-images.githubusercontent.com/53468809/112379919-0723fe00-8ce9-11eb-9f1f-8c53f84985fc.png)

# DeMon

[![.github/workflows/develop.yml](https://github.com/allow-cookies/demon/actions/workflows/develop.yml/badge.svg?branch=develop)](https://github.com/allow-cookies/demon/actions/workflows/develop.yml)

**DeMon** is a **DE**pendency **MON**itoring tool. It allows you to list and monitor all
the dependencies used across all of your projects. 

## Setup

> **Prerequisites:** Docker, docker-compose

1. Clone this repository.
1. Create `.env` file basing on the existing `.env.example` file.
1. Run `docker-compose up -d` and wait for all containers to be up and running.
1. Run migrations: `docker-compose exec django python manage.py migrate`
1. Visit http://localhost:8000 in your favourite browser.
