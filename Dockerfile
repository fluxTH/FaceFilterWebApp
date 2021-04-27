FROM python:3

WORKDIR /usr/src/app
COPY . .

RUN mkdir -p ./data/original_images && \
    mkdir -p ./data/processed_images && \
    apt-get update && apt-get install -y cmake && \
    pip install --no-cache-dir -r requirements.txt

RUN ./initialize.py

EXPOSE 12800
CMD ["./start.sh"]
