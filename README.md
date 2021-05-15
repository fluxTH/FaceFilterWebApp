# FaceFilterWebApp

This was a final project for ComEngEss in Chula CE Course.

![Screenshot](https://raw.githubusercontent.com/fluxTH/FaceFilterWebApp/main/assets/screenshot.png)

Read the [User Manual](https://github.com/fluxTH/FaceFilterWebApp/blob/main/assets/manual.pdf) for a usage guide.

## Development Server
```bash
pip3 install -r requirements.txt
./initialize.py
./server.py
```

Development server with live reload will run on http://127.0.0.1:5050/

## Production Server
```bash
docker-compose up -d
```

Production server will run on http://0.0.0.0/ and https://0.0.0.0/.

The current setup is to use a domain through CloudFlare, edit `nginx/conf/comengess.conf` to change target domain.

NOTE: The SSL certificate and keyfile in `nginx/certs` is a CloudFlare Origin Certificate, nothing is leaked here :)
