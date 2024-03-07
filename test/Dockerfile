# Use lightweight python image
FROM --platform=linux/amd64 python:3.9-slim

RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./


# Install dependencies
RUN pip install -r requirements.txt

# Copy app directory
COPY api.py .

# Command to run the application
CMD ["python", "api.py"]
