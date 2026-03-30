# Use a lightweight Python base image
FROM python:3.12-slim

ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY
ENV http_proxy=$HTTP_PROXY
ENV https_proxy=$HTTPS_PROXY

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements folder and install dependencies
# (Assuming your requirements file is named requirements.txt inside the folder)
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/requirements.txt

# Copy your source code
COPY src /app/src

# Create an empty directory where the client's data will be mounted
RUN mkdir -p /app/raw_data

# Tell Docker to run your script when the container starts
CMD ["python", "src/upload_csv_to_DSP.py"]