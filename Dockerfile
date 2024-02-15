FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./scrapy_app/requirements.txt /app/scrapy_app/requirements.txt
RUN pip install --no-cache-dir -r /app/scrapy_app/requirements.txt
COPY ./http_server/requirements.txt /app/http_server/requirements.txt
RUN pip install --no-cache-dir -r /app/http_server/requirements.txt

# Copy the application files
COPY . /app

# # RUN spider
# CMD ["scrapy","runspider", "scrapy_app/spiders/sreality_spider.py"]
# # RUN server
# CMD ["python", "http_server/app.py"]
