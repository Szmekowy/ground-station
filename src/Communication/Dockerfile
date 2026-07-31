FROM python:3.11

WORKDIR /workspace

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt


COPY . .


CMD ["python", "main.py"]