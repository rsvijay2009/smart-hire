#!/bin/bash
mkdir -p /app/uploads
chmod -R 755 /app/uploads
chown -R nobody:nobody /app/uploads
exec gunicorn run:app