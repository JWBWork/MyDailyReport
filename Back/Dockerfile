# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD [\
    "uvicorn", \
    "main:app", \
    "--ssl-keyfile", "keys/localhost.key.pem",\
    "--ssl-certfile", "keys/localhost.cert.pem",\
    "--reload", \
    "--host", "0.0.0.0", \
    "--port", "8000" \
]