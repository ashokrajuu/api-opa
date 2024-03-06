# Use lightweight python image
FROM python:3.8-slim

RUN apt update -y && apt-get install python3-dev build-essential -y

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./
COPY sqlite.db ./


# Install dependencies
RUN pip install -r requirements.txt

# Copy app directory
COPY api.py ./

# Command to run the application
CMD ["python", "api.py"]
