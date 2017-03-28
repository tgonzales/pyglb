############################################################
# Dockerfile to build Python Application Containers
# Based on Python 3.5 and Ubuntu
# Persona
############################################################

# Set the base image to Ubuntu
FROM python:3.6

# File Author / Maintainer
MAINTAINER Maintaner Cleiton Couto

# Copy the application folder inside the container
ADD . /code

# Set the default directory where CMD will execute
WORKDIR /code

# Get pip to download and install requirements:
RUN pip install -r requirements.txt
