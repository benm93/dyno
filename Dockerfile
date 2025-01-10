# Use an official Python runtime as a parent image
# FROM python:3.8
FROM continuumio/miniconda3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY environment.yml /app/
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "dyno", "/bin/bash", "-c"]

# Copy the project code into the container
COPY . /app/

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "dyno", "fastapi", "run", "backend/api.py", "--port", "80" ]

# build and run
# docker build -t condatest .
# docker run -p 8000:8000 condatest

# Note - in production build container like this so it pulls the latest:
# docker build github.com/creack/docker-firefox