#!/usr/bin/env python3

from pathlib import Path

import config
from server import db

# Create required directories
Path(config.ORIGINAL_MEDIA_PATH).mkdir(parents=True, exist_ok=True)
Path(config.PROCESSED_MEDIA_PATH).mkdir(parents=True, exist_ok=True)

# Initialize database
db.create_all()