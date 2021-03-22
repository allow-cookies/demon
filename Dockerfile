# pull official base image
FROM python:3.9-slim

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROJECT_DIR=/usr/src/app
# set work directory
WORKDIR $PROJECT_DIR

COPY requirements.txt $PROJECT_DIR
# install dependencies
RUN pip install --upgrade pip pip-tools
RUN pip-sync

# copy project
COPY ./src/ /usr/src/app/