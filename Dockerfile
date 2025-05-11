# Start from a slim Python 3.10 base image
FROM python:3.10-slim

# Install system dependencies required for Playwright and WeasyPrint
RUN apt update && apt install -y curl libnss3 libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0

# Upgrade pip to the latest version and install Python dependencies
RUN pip install --upgrade pip
RUN pip install flask trafilatura openai playwright weasyprint

# Install the Playwright browser dependencies
RUN playwright install

# Copy the project files into the Docker image
COPY . /app
WORKDIR /app

# Start the Flask app
CMD ["python", "app.py"]

