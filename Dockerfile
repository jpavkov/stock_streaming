# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (if applicable)
EXPOSE 5000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
# user .env file for environment variables
CMD ["python", "src/main.py"]
