# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any are needed for scikit-learn/numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# We add flask explicitly here just in case it's not in requirements.txt yet
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install flask

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 8081

# Make the entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Define the command to run the app
ENTRYPOINT ["./docker-entrypoint.sh"]