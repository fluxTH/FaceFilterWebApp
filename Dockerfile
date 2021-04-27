FROM python:3

WORKDIR /usr/src/app
COPY . .

RUN mkdir -p data/original_images && \
    mkdir -p data/processed_images && \
    pip install --no-cache-dir -r requirements.txt && \
    ./initialize.py

EXPOSE 12800
CMD ["./start.sh"]
