# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any are needed for scikit-learn/numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ai-phishing-detector/requirements.txt .

# Install Python dependencies
# We add flask explicitly here just in case it's not in requirements.txt yet
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from the build context
COPY . .

# Expose the app port and the phishing simulation ports
EXPOSE 4444 8080 8081 8082 8083 8084

# Make the entrypoint script executable
RUN chmod +x ai-phishing-detector/docker-entrypoint.sh

# Define the command to run the app
ENTRYPOINT ["./ai-phishing-detector/docker-entrypoint.sh"]