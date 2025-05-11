FROM python:3.10-slim
RUN apt update && apt install -y curl libnss3
RUN apt update && apt install -y curl libnss3 libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0 pip install flask trafilatura openai playwright && playwright install
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]
