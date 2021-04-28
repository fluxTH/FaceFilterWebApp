FROM python:3-buster

WORKDIR /usr/src/app
COPY . .

RUN apt-get update && apt-get install -y cmake && \
    pip3 install --no-cache-dir -r requirements.txt

RUN ./initialize.py

EXPOSE 12800
CMD ["./start.sh"]
