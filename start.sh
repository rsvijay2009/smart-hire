#!/bin/bash
mkdir -p /opt/render/project/src/uploads
chmod -R 755 /opt/render/project/src/uploads
chown -R nobody:nobody /opt/render/project/src/uploads
exec gunicorn run:app