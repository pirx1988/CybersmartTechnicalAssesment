# Base image with Python 3.8 based on Alpine linux distribution (base docker image)
FROM  python:3.12-alpine

# Set the working directory inside container with django app to /code
WORKDIR /code

# Copy requirements.txt  with list of dependencies into container
COPY requirements.txt /code/

# Update repository list
RUN apk update

# install required dependencies inside container
RUN apk add postgresql-dev gcc python3-dev musl-dev

# Install required dependencies from requirements.txt
RUN pip install -r requirements.txt

#  Copy folder from local repostiroy with project into working directory inside container
COPY . /code/


