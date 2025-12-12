FROM python:3.10-slim

# Install FFmpeg (Music ke liye) and Git
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python Libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Code
COPY . .

# Run Bot
CMD ["python", "main.py"]
