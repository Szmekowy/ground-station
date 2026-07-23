FROM python:3.11

WORKDIR /workspace

ENV PYTHONUNBUFFERED=1

# Required to display the GUI
RUN apt-get update && apt-get install -y \
    libglfw3 \
    libgl1 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
