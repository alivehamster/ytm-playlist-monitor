FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    ffmpeg \
    deno

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

CMD ["python3", "main.py"]