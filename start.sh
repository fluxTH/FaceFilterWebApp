#!/bin/bash
./initialize.py
uwsgi --ini ./uwsgi.ini
