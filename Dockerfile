# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY src/ ./src
COPY test/ ./test
COPY data/ ./data

# Set the environment variable for Python
ENV PYTHONPATH=/app/src

# Command to run your application
CMD ["python", "-m", "src.main"]
