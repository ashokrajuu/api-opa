FROM python:3.8-slim

RUN apt update -y && apt-get install python3-dev build-essential -y

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src/api/api.py ./

CMD ["python", "api.py"]
