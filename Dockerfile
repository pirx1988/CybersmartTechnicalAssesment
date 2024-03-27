# Base image with Python 3.8 based on Alpine linux distribution
FROM  python:3.12-alpine

# Set the working directory to of todoListApp to /code
WORKDIR /code

# Copy requirements.txt  with list of dependencies into container
COPY requirements.txt /code/

# update repository list
RUN apk update
# install required dependencies inside alpine based container
RUN apk add postgresql-dev gcc python3-dev musl-dev

# Install required dependencies from requirements.txt
RUN pip install -r requirements.txt

#  Copy folder with project into workdir container's folder
COPY . /code/


