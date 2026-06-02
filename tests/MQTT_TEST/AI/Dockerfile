FROM python:3.11

WORKDIR /workspace

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]